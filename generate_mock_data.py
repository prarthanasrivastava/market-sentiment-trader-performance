import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
import random

def generate_mock_data():
    """Generates mock data for the Market Sentiment Trader Performance project."""
    
    # 1. Create Directories
    os.makedirs('data', exist_ok=True)
    
    print("Generating mock data...")

    # 2. Generate Date Range
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)
    date_range = pd.date_range(start_date, end_date)
    
    # 3. Generate Sentiment Data (fear_greed_index.csv)
    # Columns: date, classification
    sentiments = ['Extreme Fear', 'Fear', 'Neutral', 'Greed', 'Extreme Greed']
    
    sentiment_data = {
        'date': date_range,
        'classification': np.random.choice(sentiments, size=len(date_range), p=[0.1, 0.2, 0.4, 0.2, 0.1])
    }
    sentiment_df = pd.DataFrame(sentiment_data)
    sentiment_df.to_csv('data/fear_greed_index.csv', index=False)
    print(f"Created data/fear_greed_index.csv with {len(sentiment_df)} rows.")

    # 4. Generate Trader Data (historical_data.csv)
    # Columns typically found in trade logs: Timestamp IST, Closed PnL, Size USD, Side
    
    num_trades = 500
    trade_dates = [start_date + timedelta(days=random.randint(0, 364), hours=random.randint(0, 23), minutes=random.randint(0, 59)) for _ in range(num_trades)]
    trade_dates.sort()
    
    trade_data = {
        'Timestamp IST': [d.strftime('%d-%m-%Y %H:%M') for d in trade_dates],
        'Closed PnL': np.random.normal(loc=10, scale=100, size=num_trades), # Mean profit $10, std dev $100
        'Size USD': np.random.uniform(100, 5000, size=num_trades),
        'Side': np.random.choice(['Buy', 'Sell'], size=num_trades)
    }
    
    # Introduce some correlation for the analysis to pick up
    # e.g., slightly higher profits on Greed days (simulated by checking date match)
    # For simplicity, we just save the random data, the analysis might show "random" results which is fine for a mock.
    
    trader_df = pd.DataFrame(trade_data)
    trader_df.to_csv('data/historical_data.csv', index=False)
    print(f"Created data/historical_data.csv with {len(trader_df)} rows.")
    
if __name__ == "__main__":
    generate_mock_data()
