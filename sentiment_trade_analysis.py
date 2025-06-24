
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load datasets
trader_df = pd.read_csv('data/historical_data.csv')
sentiment_df = pd.read_csv('data/fear_greed_index.csv')

# Preprocessing
trader_df['Trade Datetime'] = pd.to_datetime(trader_df['Timestamp IST'], format='%d-%m-%Y %H:%M')
trader_df['Trade Date'] = trader_df['Trade Datetime'].dt.date
sentiment_df['Sentiment Date'] = pd.to_datetime(sentiment_df['date']).dt.date

# Merge datasets
merged_df = pd.merge(trader_df, sentiment_df, left_on='Trade Date', right_on='Sentiment Date', how='left')
merged_df = merged_df.dropna(subset=['classification'])

# Feature engineering
merged_df['PnL per USD'] = merged_df['Closed PnL'] / merged_df['Size USD']
merged_df['Profit'] = merged_df['Closed PnL'] > 0

# Analysis
pnl_by_sentiment = merged_df.groupby('classification')['Closed PnL'].describe()
profit_rate = merged_df.groupby('classification')['Profit'].mean() * 100
average_size = merged_df.groupby('classification')['Size USD'].mean()
side_distribution = merged_df.groupby(['classification', 'Side']).size().unstack(fill_value=0)

# Save summary statistics
os.makedirs('outputs/plots', exist_ok=True)
pnl_by_sentiment.to_csv('outputs/pnl_by_sentiment_summary.csv')

# Visualization - Profit Rate
plt.figure(figsize=(10, 6))
sns.barplot(x=profit_rate.index, y=profit_rate.values, palette='viridis')
plt.ylabel('Profit Rate (%)')
plt.title('Profit Rate by Market Sentiment')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('outputs/plots/profit_rate_by_sentiment.png')
plt.close()

# Visualization - Average Size
plt.figure(figsize=(10, 6))
sns.barplot(x=average_size.index, y=average_size.values, palette='magma')
plt.ylabel('Average Trade Size (USD)')
plt.title('Average Trade Size by Market Sentiment')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('outputs/plots/average_trade_size_by_sentiment.png')
plt.close()

# Visualization - Trade Side Distribution
side_distribution.plot(kind='bar', stacked=True, figsize=(12, 7), colormap='coolwarm')
plt.ylabel('Number of Trades')
plt.title('Trade Side Distribution by Market Sentiment')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('outputs/plots/trade_side_distribution.png')
plt.close()

print("Analysis complete. Results saved in 'outputs' folder.")
