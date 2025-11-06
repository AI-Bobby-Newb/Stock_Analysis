# Stock Analysis & Prediction System

A comprehensive stock analysis and prediction system that provides actionable insights with scoring and sentiment analysis using **FREE data sources**.

## Features

### 🎯 Core Capabilities

1. **Comprehensive Stock Scoring** (0-100 scale with 1-5 star ratings)
   - Technical Analysis (RSI, MACD, Moving Averages, Bollinger Bands, ADX)
   - Fundamental Analysis (P/E, PEG, ROE, Margins, Growth Rates)
   - Sentiment Analysis (News sentiment + Market indicators)
   - Momentum Analysis (Short, medium, and long-term trends)

2. **Multi-Timeframe Predictions**
   - Tomorrow's predicted movement
   - Weekly outlook
   - 12-month long-term projections

3. **Smart Recommendations**
   - "Should I buy?" analysis for any stock
   - Entry point identification
   - Target price and stop loss calculations
   - Risk/reward ratios

4. **Specialized Lists**
   - Top overall picks
   - Predicted top gainers for tomorrow
   - Best value stocks
   - Best tech stocks
   - Weekly picks
   - Monthly picks
   - Long-term investment recommendations
   - Stocks to buy right now

### 📊 Data Sources (100% Free)

- **Yahoo Finance** (via yfinance) - Price data, fundamentals, news
- **Technical Analysis** - Built-in indicators (ta library)
- **Sentiment Analysis** - Natural language processing (TextBlob)

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd Stock_Analysis

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Basic Commands

#### Analyze a Specific Stock (e.g., AAPL)
```bash
python stock_predictions.py --analyze AAPL
```

**Output includes:**
- Overall score and star rating (1-5 stars)
- Component scores (technical, fundamental, sentiment, momentum)
- Current price and target prices
- Predictions (tomorrow, next week, 12 months)
- Entry signal and buy recommendation
- Key financial metrics
- Sentiment analysis

#### Should I Buy This Stock?
```bash
python stock_predictions.py --should-buy AAPL
```

**Provides:**
- Clear YES/NO/MAYBE recommendation
- Reasoning based on score and entry point
- Target price and stop loss
- Risk analysis

### Recommendation Lists

#### Top Stock Picks
```bash
python stock_predictions.py --top-picks 10
```
Best overall stocks based on comprehensive scoring.

#### Predicted Top Gainers for Tomorrow
```bash
python stock_predictions.py --top-gainers 10
```
Stocks predicted to rise tomorrow based on momentum and technical indicators.

#### Best Value Picks
```bash
python stock_predictions.py --best-value 10
```
Undervalued stocks with strong fundamentals.

#### Best Tech Stocks
```bash
python stock_predictions.py --tech-stocks 10
```
Top technology sector stocks to buy now.

#### Weekly Picks
```bash
python stock_predictions.py --weekly-picks 10
```
Best stocks for the coming week based on short-term momentum.

#### Long-Term Investment Picks
```bash
python stock_predictions.py --long-term
```
Quality stocks suitable for long-term holding (12+ months).

#### Stocks to Buy Right Now
```bash
python stock_predictions.py --buy-now
```
High-scoring stocks at good entry points for immediate purchase.

#### Monthly Picks
```bash
python stock_predictions.py --monthly 10
```
Best picks for the month ahead.

## Scoring System

### Overall Score (0-100)
Weighted combination of four components:

- **Technical Analysis (35%)**: Chart patterns, indicators, trends
- **Fundamental Analysis (35%)**: Financial health, valuation metrics
- **Sentiment Analysis (20%)**: News sentiment, market sentiment
- **Momentum (10%)**: Recent price movements

### Star Ratings
- ⭐⭐⭐⭐⭐ (5 stars): Score 80+ - **Strong Buy**
- ⭐⭐⭐⭐☆ (4 stars): Score 65-79 - **Buy**
- ⭐⭐⭐☆☆ (3 stars): Score 50-64 - **Hold**
- ⭐⭐☆☆☆ (2 stars): Score 35-49 - **Sell**
- ⭐☆☆☆☆ (1 star): Score 0-34 - **Strong Sell**

## Technical Indicators Used

- **RSI (Relative Strength Index)**: Overbought/oversold conditions
- **MACD**: Trend direction and momentum
- **Moving Averages**: SMA 20, SMA 50 for trend identification
- **Bollinger Bands**: Volatility and price levels
- **ADX**: Trend strength
- **Volume Analysis**: Trading volume trends

## Fundamental Metrics Analyzed

- P/E Ratio (Price-to-Earnings)
- PEG Ratio (Price/Earnings to Growth)
- Price-to-Book Ratio
- Debt-to-Equity Ratio
- Return on Equity (ROE)
- Profit Margins
- Revenue Growth
- Dividend Yield
- Beta (volatility measure)

## Sentiment Analysis

The system analyzes:
- **News Sentiment**: Recent news articles about the stock
- **Market Sentiment**: Price/volume patterns, momentum indicators
- **Overall Sentiment**: Combined score from multiple sources

Sentiment Ratings:
- Very Bullish (75-100)
- Bullish (60-74)
- Neutral (40-59)
- Bearish (25-39)
- Very Bearish (0-24)

## Entry Point Signals

- **Strong Buy Now**: High score + excellent entry point
- **Good Entry Point**: Good score + favorable technical setup
- **Consider Buying**: Reasonable opportunity
- **Wait for Better Entry**: Wait for improved conditions

## Examples

### Example 1: Detailed Analysis
```bash
python stock_predictions.py --analyze MSFT
```

Output:
```
================================================================================
  Detailed Analysis: MSFT
================================================================================

────────────────────────────────────────────────────────────────────────────────
  MSFT - Microsoft Corporation
  Sector: Technology | Industry: Software
────────────────────────────────────────────────────────────────────────────────

  OVERALL SCORE: 78.5/100  ★★★★☆
  RATING: Buy

  Current Price: $378.91
  Target Price:  $435.74
  Stop Loss:     $350.60
  Upside:        15.0%

  Component Scores:
    Technical:    82.3/100
    Fundamental:  76.8/100
    Sentiment:    75.2/100
    Momentum:     80.1/100

  Predictions:
    Tomorrow:  Up 0.45% ($380.62) [Confidence: 68%]
    Next Week: Up 2.1% ($386.86)
    12 Months: Bullish 18.5% ($448.98)

  Entry Signal: Good Entry Point
  RSI: 58.3 | 52W Position: 72.5%

  Sentiment: Bullish (75.2/100)
```

### Example 2: Should I Buy?
```bash
python stock_predictions.py --should-buy AAPL
```

Output:
```
  ============================================================================
   RECOMMENDATION: YES - Strong Buy
  ============================================================================

  High score (82.3/100) and good entry point. Bullish sentiment.

  Current Price: $178.45
  Target Price:  $223.06
  Stop Loss:     $165.02
  Overall Score: 82.3/100
```

### Example 3: Top Picks
```bash
python stock_predictions.py --top-picks 5
```

Output shows a table with the 5 best stocks across all analyzed tickers.

## Python API Usage

You can also use the system programmatically:

```python
from src.stock_analyzer import StockAnalyzer

# Initialize analyzer
analyzer = StockAnalyzer()

# Analyze a single stock
analysis = analyzer.analyze_stock('AAPL', timeframe='1y')
print(f"Score: {analysis['overall_score']['overall_score']}")

# Should I buy?
decision = analyzer.should_buy_now('AAPL')
print(f"Recommendation: {decision['recommendation']}")

# Get top picks
data_source = analyzer.data_source
symbols = data_source.get_trending_tickers()
top_picks = analyzer.get_top_picks(symbols, count=10)

# Get predicted top gainers
gainers = analyzer.get_top_gainers_prediction(symbols, count=10)

# Get best value stocks
value_picks = analyzer.get_best_value(symbols, count=10)
```

## Project Structure

```
Stock_Analysis/
├── src/
│   ├── __init__.py
│   ├── data_sources.py         # Free data source integrations
│   ├── sentiment_analyzer.py   # Sentiment analysis engine
│   ├── stock_scorer.py         # Scoring algorithms
│   ├── predictor.py            # Prediction engine
│   └── stock_analyzer.py       # Main analysis orchestrator
├── stock_predictions.py        # CLI interface
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── LICENSE
```

## Disclaimer

⚠️ **IMPORTANT**: This tool is for educational and informational purposes only. It is NOT financial advice. The predictions and recommendations are based on historical data and technical analysis, which cannot guarantee future results.

**Always:**
- Do your own research (DYOR)
- Consult with a licensed financial advisor
- Never invest more than you can afford to lose
- Understand that all investments carry risk
- Past performance does not guarantee future results

The creators and contributors of this tool are not responsible for any financial losses incurred from using this software.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## License

See LICENSE file for details.

## Acknowledgments

- **yfinance**: Yahoo Finance data API
- **ta**: Technical analysis library
- **TextBlob**: Natural language processing
- **pandas, numpy, scikit-learn**: Data processing and analysis

## Support

For questions or issues, please open an issue on GitHub.

---

**Made with ❤️ for the trading community**

*Using 100% free data sources - No API keys required!*
