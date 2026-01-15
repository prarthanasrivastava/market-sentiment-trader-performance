# Bitcoin Market Sentiment and Trader Performance Analysis

## Project Overview
This project explores the relationship between **Bitcoin market sentiment** (Fear & Greed Index) and **trader performance**. By analyzing historical trade data alongside market sentiment, we aim to uncover behavioral patterns and performance correlations.

## Key Insights
Preliminary analysis of the data suggests:
- **Profit Rates** may vary significantly during extreme sentiment periods (Extreme Fear vs. Extreme Greed).
- **Trade Sizes** often adjust based on market confidence.
- **Trading Activity** (Buy vs. Sell frequency) shifts with market sentiment.

## Folder Structure
```
.
├── data/
│   ├── historical_data.csv       # (Generated/User Provided) Trade history
│   └── fear_greed_index.csv      # (Generated/User Provided) Sentiment data
├── outputs/
│   ├── plots/                    # Generated visualization charts
│   └── sentiment_performance_summary.csv  # aggregated performance metrics
├── sentiment_trade_analysis.py   # Main analysis script
├── generate_mock_data.py         # Script to create mock data for testing
├── requirements.txt              # Project dependencies
└── README.md                     # Project documentation
```

## How to Run

### 1. Setup Environment
Install the required dependencies:
```bash
pip install -r requirements.txt
```

### 2. Prepare Data
**Option A: Run with Mock Data (Quick Start)**
If you don't have your own data yet, generate realistic mock data:
```bash
python generate_mock_data.py
```

**Option B: Use Real Data**
Place your files in the `data/` folder:
- `historical_data.csv`: Must contain `Timestamp IST`, `Closed PnL`, `Size USD`, `Side`.
- `fear_greed_index.csv`: Must contain `date`, `classification`.

### 3. Run Analysis
Execute the main script to process data and generate insights:
```bash
python sentiment_trade_analysis.py
```

### 4. View Results
Check the `outputs/` folder for the summary CSV and `outputs/plots/` for visual charts.
