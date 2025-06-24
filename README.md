
# Bitcoin Market Sentiment and Trader Performance Analysis

## Project Overview
This project explores the relationship between Bitcoin market sentiment and trader performance using two datasets:
- **Bitcoin Market Sentiment Dataset:** Contains daily sentiment classifications (Fear, Greed, etc.).
- **Historical Trader Data:** Contains execution details, PnL, trade size, and more.

## Key Findings
- Traders tend to have **higher profit rates during Extreme Greed** days.
- Average trade size is **largest during Fear** days.
- **Buy and Sell distributions** vary by sentiment, with balanced trades during Neutral periods.

## Repository Structure
```
.
├── data/
│   ├── historical_data.csv
│   └── fear_greed_index.csv
├── notebooks/
│   └── analysis.ipynb
├── outputs/
│   ├── plots/
│   │   ├── profit_rate_by_sentiment.png
│   │   ├── average_trade_size_by_sentiment.png
│   │   └── trade_side_distribution.png
│   └── pnl_by_sentiment_summary.csv
├── sentiment_trade_analysis.py
├── README.md
└── requirements.txt
```

## How to Run
1. Install required packages:
```bash
pip install -r requirements.txt
```
2. Run the Python script:
```bash
python sentiment_trade_analysis.py
```
3. Check the `outputs/plots` folder for generated visuals.

## Requirements
- pandas
- matplotlib
- seaborn

---

*Project completed as part of a market analysis assignment.*
