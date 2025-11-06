#!/usr/bin/env python3
"""
Stock Prediction and Analysis System
Provides comprehensive stock analysis with scoring and predictions
"""

import argparse
import sys
from datetime import datetime
from tabulate import tabulate
from src.stock_analyzer import StockAnalyzer


def print_header(text: str):
    """Print formatted header"""
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80)


def print_stock_summary(analysis: dict):
    """Print summary of stock analysis"""
    print(f"\n{'─' * 80}")
    print(f"  {analysis['symbol']} - {analysis['name']}")
    print(f"  Sector: {analysis['sector']} | Industry: {analysis['industry']}")
    print(f"{'─' * 80}")

    # Overall Score
    overall = analysis['overall_score']
    stars = '★' * overall['stars'] + '☆' * (5 - overall['stars'])
    print(f"\n  OVERALL SCORE: {overall['overall_score']:.1f}/100  {stars}")
    print(f"  RATING: {overall['rating']}")

    # Current Price and Targets
    print(f"\n  Current Price: ${analysis['current_price']:.2f}")
    if 'targets' in analysis and analysis['targets']:
        print(f"  Target Price:  ${analysis['targets'].get('target_price', 'N/A')}")
        print(f"  Stop Loss:     ${analysis['targets'].get('stop_loss', 'N/A')}")
        print(f"  Upside:        {analysis['targets'].get('upside_potential', 'N/A')}%")

    # Component Scores
    print(f"\n  Component Scores:")
    scores = overall['component_scores']
    print(f"    Technical:    {scores['technical']:.1f}/100")
    print(f"    Fundamental:  {scores['fundamental']:.1f}/100")
    print(f"    Sentiment:    {scores['sentiment']:.1f}/100")
    print(f"    Momentum:     {scores['momentum']:.1f}/100")

    # Predictions
    print(f"\n  Predictions:")
    tomorrow = analysis['predictions']['tomorrow']
    print(f"    Tomorrow:  {tomorrow['direction']} {abs(tomorrow['predicted_change_pct']):.2f}% "
          f"(${tomorrow['predicted_price']:.2f}) [Confidence: {tomorrow['confidence']:.0f}%]")

    next_week = analysis['predictions']['next_week']
    print(f"    Next Week: {next_week['direction']} {abs(next_week['predicted_change_pct']):.2f}% "
          f"(${next_week['predicted_price']:.2f})")

    long_term = analysis['predictions']['long_term']
    print(f"    12 Months: {long_term['direction']} {abs(long_term['predicted_change_pct']):.2f}% "
          f"(${long_term['predicted_price']:.2f})")

    # Entry Signal
    entry = analysis['entry_point']
    print(f"\n  Entry Signal: {entry['entry_signal']}")
    print(f"  RSI: {entry.get('rsi', 'N/A'):.1f} | 52W Position: {entry.get('52w_range_position', 'N/A'):.1f}%")

    # Sentiment
    sentiment = analysis['sentiment']
    print(f"\n  Sentiment: {sentiment['sentiment_rating']} "
          f"({sentiment['overall_sentiment_score']:.1f}/100)")


def print_stock_table(analyses: list, title: str = "Stock Analysis"):
    """Print table of multiple stock analyses"""
    print_header(title)

    table_data = []
    for analysis in analyses:
        overall = analysis['overall_score']
        tomorrow = analysis['predictions']['tomorrow']

        row = [
            analysis['symbol'],
            f"${analysis['current_price']:.2f}",
            f"{overall['overall_score']:.1f}",
            overall['rating'],
            '★' * overall['stars'],
            f"{tomorrow['direction']} {abs(tomorrow['predicted_change_pct']):.1f}%",
            analysis['sentiment']['sentiment_rating'],
            analysis['entry_point']['entry_signal'],
        ]
        table_data.append(row)

    headers = ['Symbol', 'Price', 'Score', 'Rating', 'Stars', 'Tomorrow', 'Sentiment', 'Entry Signal']
    print(tabulate(table_data, headers=headers, tablefmt='grid'))


def analyze_specific_stock(analyzer: StockAnalyzer, symbol: str):
    """Analyze a specific stock in detail"""
    print_header(f"Detailed Analysis: {symbol}")

    analysis = analyzer.analyze_stock(symbol, timeframe='1y')
    if not analysis:
        print(f"\nError: Could not analyze {symbol}")
        return

    print_stock_summary(analysis)

    # Additional Details
    print(f"\n  Key Metrics:")
    metrics = analysis['metrics']
    if metrics:
        if metrics.get('pe_ratio'):
            print(f"    P/E Ratio:        {metrics['pe_ratio']:.2f}")
        if metrics.get('peg_ratio'):
            print(f"    PEG Ratio:        {metrics['peg_ratio']:.2f}")
        if metrics.get('price_to_book'):
            print(f"    Price/Book:       {metrics['price_to_book']:.2f}")
        if metrics.get('roe'):
            print(f"    ROE:              {metrics['roe']*100:.2f}%")
        if metrics.get('profit_margin'):
            print(f"    Profit Margin:    {metrics['profit_margin']*100:.2f}%")
        if metrics.get('revenue_growth'):
            print(f"    Revenue Growth:   {metrics['revenue_growth']*100:.2f}%")
        if metrics.get('dividend_yield'):
            print(f"    Dividend Yield:   {metrics['dividend_yield']*100:.2f}%")

    print("\n")


def should_i_buy(analyzer: StockAnalyzer, symbol: str):
    """Provide buy recommendation for a stock"""
    print_header(f"Should I Buy {symbol}?")

    result = analyzer.should_buy_now(symbol)

    print(f"\n  {'=' * 76}")
    print(f"   RECOMMENDATION: {result['recommendation']}")
    print(f"  {'=' * 76}")
    print(f"\n  {result['reason']}")
    print(f"\n  Current Price: ${result['current_price']:.2f}")
    print(f"  Target Price:  ${result.get('target_price', 'N/A')}")
    print(f"  Stop Loss:     ${result.get('stop_loss', 'N/A')}")
    print(f"  Overall Score: {result['score']:.1f}/100")

    print("\n")


def get_top_picks(analyzer: StockAnalyzer, count: int = 10):
    """Get top stock picks"""
    data_source = analyzer.data_source
    symbols = data_source.get_trending_tickers()

    top_picks = analyzer.get_top_picks(symbols, count=count)
    print_stock_table(top_picks, f"Top {count} Stock Picks")

    print("\n  Top 3 Recommendations:")
    for i, pick in enumerate(top_picks[:3], 1):
        print(f"\n  {i}. {pick['symbol']} - {pick['name']}")
        print(f"     Score: {pick['overall_score']['overall_score']:.1f}/100 | "
              f"Rating: {pick['overall_score']['rating']}")
        print(f"     Price: ${pick['current_price']:.2f} → "
              f"Target: ${pick['targets'].get('target_price', 'N/A')}")


def get_top_gainers(analyzer: StockAnalyzer, count: int = 10):
    """Get predicted top gainers for tomorrow"""
    data_source = analyzer.data_source
    symbols = data_source.get_trending_tickers()

    gainers = analyzer.get_top_gainers_prediction(symbols, count=count)
    print_stock_table(gainers, f"Predicted Top {count} Gainers for Tomorrow")


def get_best_value(analyzer: StockAnalyzer, count: int = 10):
    """Get best value stock picks"""
    data_source = analyzer.data_source
    symbols = data_source.get_trending_tickers()

    value_picks = analyzer.get_best_value(symbols, count=count)
    print_stock_table(value_picks, f"Best {count} Value Picks")


def get_tech_stocks(analyzer: StockAnalyzer, count: int = 10):
    """Get best tech stocks to buy"""
    data_source = analyzer.data_source
    symbols = data_source.get_tech_stocks()

    print(f"\nAnalyzing {len(symbols)} tech stocks...")
    analyses = analyzer.analyze_multiple(symbols, timeframe='1y')
    ranked = analyzer.rank_stocks(analyses, 'overall_score')

    print_stock_table(ranked[:count], f"Best {count} Tech Stocks to Buy Now")


def weekly_picks(analyzer: StockAnalyzer, count: int = 10):
    """Get stock picks for the week"""
    data_source = analyzer.data_source
    symbols = data_source.get_trending_tickers()

    print(f"\nAnalyzing stocks for weekly performance...")
    analyses = analyzer.analyze_multiple(symbols, timeframe='3mo')

    # Filter for stocks with good momentum and score
    weekly = [a for a in analyses if a['overall_score']['overall_score'] >= 55]
    ranked = sorted(weekly, key=lambda x: (
        x['overall_score']['overall_score'],
        x['predictions']['next_week']['predicted_change_pct']
    ), reverse=True)

    print_stock_table(ranked[:count], f"Top {count} Stock Picks for This Week")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Stock Prediction and Analysis System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --analyze AAPL              Detailed analysis of AAPL
  %(prog)s --should-buy AAPL           Should I buy AAPL now?
  %(prog)s --top-picks 10              Top 10 stock picks
  %(prog)s --top-gainers 10            Predicted top 10 gainers for tomorrow
  %(prog)s --best-value 10             Best 10 value picks
  %(prog)s --tech-stocks 10            Best 10 tech stocks
  %(prog)s --weekly-picks 10           Top 10 picks for the week
  %(prog)s --long-term                 Long-term investment recommendations
  %(prog)s --buy-now                   Stocks to buy right now
        """
    )

    parser.add_argument('--analyze', metavar='SYMBOL',
                       help='Analyze a specific stock')
    parser.add_argument('--should-buy', metavar='SYMBOL',
                       help='Should I buy this stock now?')
    parser.add_argument('--top-picks', type=int, metavar='N',
                       help='Get top N stock picks')
    parser.add_argument('--top-gainers', type=int, metavar='N',
                       help='Predicted top N gainers for tomorrow')
    parser.add_argument('--best-value', type=int, metavar='N',
                       help='Best N value stock picks')
    parser.add_argument('--tech-stocks', type=int, metavar='N',
                       help='Best N tech stocks to buy')
    parser.add_argument('--weekly-picks', type=int, metavar='N',
                       help='Top N stock picks for the week')
    parser.add_argument('--long-term', action='store_true',
                       help='Long-term investment recommendations')
    parser.add_argument('--buy-now', action='store_true',
                       help='Stocks to buy right now (high score + good entry)')
    parser.add_argument('--monthly', type=int, metavar='N',
                       help='Best N picks for the month')

    args = parser.parse_args()

    # Show usage if no arguments
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    # Initialize analyzer
    print_header("Stock Prediction & Analysis System")
    print(f"  Powered by free data sources")
    print(f"  Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    analyzer = StockAnalyzer()

    # Process commands
    if args.analyze:
        analyze_specific_stock(analyzer, args.analyze.upper())

    if args.should_buy:
        should_i_buy(analyzer, args.should_buy.upper())

    if args.top_picks:
        get_top_picks(analyzer, args.top_picks)

    if args.top_gainers:
        get_top_gainers(analyzer, args.top_gainers)

    if args.best_value:
        get_best_value(analyzer, args.best_value)

    if args.tech_stocks:
        get_tech_stocks(analyzer, args.tech_stocks)

    if args.weekly_picks:
        weekly_picks(analyzer, args.weekly_picks)

    if args.monthly:
        get_best_value(analyzer, args.monthly)

    if args.long_term:
        print_header("Long-Term Investment Recommendations")
        data_source = analyzer.data_source
        symbols = data_source.get_trending_tickers()

        analyses = analyzer.analyze_multiple(symbols, timeframe='2y')
        # Filter for quality long-term holds
        long_term = [a for a in analyses
                    if a['overall_score']['overall_score'] >= 60
                    and a['fundamental']['score'] >= 55]
        ranked = sorted(long_term, key=lambda x: x['overall_score']['overall_score'], reverse=True)

        print_stock_table(ranked[:10], "Top 10 Long-Term Investment Picks")

    if args.buy_now:
        print_header("Stocks to Buy Right Now")
        data_source = analyzer.data_source
        symbols = data_source.get_trending_tickers()

        analyses = analyzer.analyze_multiple(symbols, timeframe='6mo')
        # Filter for strong buy signals
        buy_now = [a for a in analyses
                  if a['overall_score']['overall_score'] >= 65
                  and a['entry_point']['entry_signal'] in ['Strong Buy Now', 'Good Entry Point']]
        ranked = sorted(buy_now, key=lambda x: x['overall_score']['overall_score'], reverse=True)

        print_stock_table(ranked[:10], "Top 10 Stocks to Buy Right Now")


if __name__ == '__main__':
    main()
