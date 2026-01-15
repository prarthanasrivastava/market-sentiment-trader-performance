import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
import logging

# --- Configuration ---
DATA_DIR = "data"
OUTPUT_DIR = "outputs"
PLOTS_DIR = os.path.join(OUTPUT_DIR, "plots")
HISTORICAL_DATA_FILE = "historical_data.csv"
SENTIMENT_DATA_FILE = "fear_greed_index.csv"

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

def load_data():
    """Loads datasets from the data folder."""
    try:
        data_path = os.path.join(DATA_DIR, HISTORICAL_DATA_FILE)
        sentiment_path = os.path.join(DATA_DIR, SENTIMENT_DATA_FILE)

        if not os.path.exists(data_path) or not os.path.exists(sentiment_path):
            logger.error("Data files not found.")
            logger.info("Please run 'python generate_mock_data.py' first to generate sample data,")
            logger.info(f"or place your '{HISTORICAL_DATA_FILE}' and '{SENTIMENT_DATA_FILE}' in the '{DATA_DIR}/' folder.")
            sys.exit(1)

        trader_df = pd.read_csv(data_path)
        sentiment_df = pd.read_csv(sentiment_path)
        logger.info("Data loaded successfully.")
        return trader_df, sentiment_df
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        sys.exit(1)

def preprocess_data(trader_df, sentiment_df):
    """Cleans and merges the datasets."""
    # Convert timestamps
    try:
        trader_df['Trade Datetime'] = pd.to_datetime(trader_df['Timestamp IST'], format='%d-%m-%Y %H:%M')
    except ValueError:
        logger.warning("Date format mismatch in historical_data.csv. Trying auto-inference.")
        trader_df['Trade Datetime'] = pd.to_datetime(trader_df['Timestamp IST'])

    trader_df['Trade Date'] = trader_df['Trade Datetime'].dt.date
    
    # Process sentiment dates
    date_col = 'date' if 'date' in sentiment_df.columns else sentiment_df.columns[0]
    sentiment_df['Sentiment Date'] = pd.to_datetime(sentiment_df[date_col]).dt.date
    
    # Merge
    merged_df = pd.merge(trader_df, sentiment_df, left_on='Trade Date', right_on='Sentiment Date', how='left')
    
    # Filter out trades with no matching sentiment
    merged_df = merged_df.dropna(subset=['classification'])
    
    # Feature Engineering
    if 'Size USD' in merged_df.columns and 'Closed PnL' in merged_df.columns:
        merged_df['PnL per USD'] = merged_df['Closed PnL'] / merged_df['Size USD']
        merged_df['Profit'] = merged_df['Closed PnL'] > 0
    
    logger.info(f"Processed {len(merged_df)} trades linked with sentiment data.")
    return merged_df

def analyze_data(merged_df):
    """Calculates summary statistics."""
    if 'classification' not in merged_df.columns:
        logger.error("'classification' column missing.")
        return None, None, None, None

    # Groupby operations
    pnl_by_sentiment = merged_df.groupby('classification')['Closed PnL'].describe()
    profit_rate = merged_df.groupby('classification')['Profit'].mean() * 100
    average_size = merged_df.groupby('classification')['Size USD'].mean()
    side_distribution = merged_df.groupby(['classification', 'Side']).size().unstack(fill_value=0)
    
    return pnl_by_sentiment, profit_rate, average_size, side_distribution

def visualize_data(pnl_by_sentiment, profit_rate, average_size, side_distribution):
    """Generates and saves plots and summary CSV."""
    os.makedirs(PLOTS_DIR, exist_ok=True)
    
    # 1. Save Summary CSV (Consolidated)
    summary_df = pnl_by_sentiment.copy()
    summary_df['Profit Rate (%)'] = profit_rate
    summary_df['Average Trade Size ($)'] = average_size
    
    # Select key columns for the summary report
    summary_report = summary_df[['count', 'mean', 'Profit Rate (%)', 'Average Trade Size ($)']].rename(columns={
        'count': 'Trade Count',
        'mean': 'Average PnL ($)'
    })
    
    summary_path = os.path.join(OUTPUT_DIR, 'sentiment_performance_summary.csv')
    summary_report.to_csv(summary_path)
    logger.info(f"Summary CSV saved to: {summary_path}")

    # 2. Profit Rate Plot
    plt.figure(figsize=(10, 6))
    sns.barplot(x=profit_rate.index, y=profit_rate.values, palette='viridis')
    plt.ylabel('Profit Rate (%)')
    plt.title('Profit Rate by Market Sentiment')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, 'profit_rate_by_sentiment.png'))
    plt.close()
    
    # 3. Average Size Plot
    plt.figure(figsize=(10, 6))
    sns.barplot(x=average_size.index, y=average_size.values, palette='magma')
    plt.ylabel('Average Trade Size (USD)')
    plt.title('Average Trade Size by Market Sentiment')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, 'average_trade_size_by_sentiment.png'))
    plt.close()
    
    # 4. Trade Side Distribution Plot
    side_distribution.plot(kind='bar', stacked=True, figsize=(12, 7), colormap='coolwarm')
    plt.ylabel('Number of Trades')
    plt.title('Trade Side Distribution by Market Sentiment')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, 'trade_side_distribution.png'))
    plt.close()
    
    logger.info(f"Visualizations saved to: {PLOTS_DIR}")

def main():
    logger.info("Starting Market Sentiment Trade Analysis...")
    trader_df, sentiment_df = load_data()
    merged_df = preprocess_data(trader_df, sentiment_df)
    
    if merged_df.empty:
        logger.warning("No matches found between Trade Date and Sentiment Date.")
        return

    pnl_by_sentiment, profit_rate, average_size, side_distribution = analyze_data(merged_df)
    
    if pnl_by_sentiment is not None:
        visualize_data(pnl_by_sentiment, profit_rate, average_size, side_distribution)
    
    logger.info("Analysis run finished.")

if __name__ == "__main__":
    main()
