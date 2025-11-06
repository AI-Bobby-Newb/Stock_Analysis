"""
Main stock analyzer
Combines all components to provide comprehensive stock analysis
"""

from .data_sources import StockDataSource
from .sentiment_analyzer import SentimentAnalyzer
from .stock_scorer import StockScorer
from .predictor import StockPredictor
from typing import Dict, List, Optional
import pandas as pd


class StockAnalyzer:
    """Main stock analysis engine"""

    def __init__(self):
        self.data_source = StockDataSource()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.scorer = StockScorer()
        self.predictor = StockPredictor()

    def analyze_stock(self, symbol: str, timeframe: str = '1y') -> Optional[Dict]:
        """
        Perform comprehensive analysis on a stock

        Args:
            symbol: Stock ticker symbol
            timeframe: Data timeframe (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y)

        Returns:
            Dictionary with complete analysis or None if error
        """
        print(f"\nAnalyzing {symbol}...")

        # Fetch data
        data = self.data_source.get_stock_data(symbol, timeframe)
        if data is None or data.empty:
            print(f"Could not fetch data for {symbol}")
            return None

        info = self.data_source.get_stock_info(symbol)
        metrics = self.data_source.get_financial_metrics(symbol)

        # Perform analyses
        print("  - Technical analysis...")
        technical = self.scorer.calculate_technical_score(data)

        print("  - Fundamental analysis...")
        fundamental = self.scorer.calculate_fundamental_score(metrics)

        print("  - Sentiment analysis...")
        sentiment = self.sentiment_analyzer.get_overall_sentiment(symbol, data)

        print("  - Momentum analysis...")
        momentum = self.scorer.calculate_momentum_score(data)

        print("  - Overall scoring...")
        overall = self.scorer.calculate_overall_score(technical, fundamental, sentiment, momentum)

        print("  - Predictions...")
        short_term = self.predictor.predict_short_term(data, days=1)
        weekly = self.predictor.predict_medium_term(data, weeks=1)
        long_term = self.predictor.predict_long_term(data, months=12)

        print("  - Entry point analysis...")
        current_price = data['Close'].iloc[-1]
        entry = self.predictor.identify_entry_point(data, overall['overall_score'])
        targets = self.predictor.calculate_target_price(current_price, overall['overall_score'], long_term)

        return {
            'symbol': symbol,
            'name': info.get('longName', symbol),
            'sector': info.get('sector', 'N/A'),
            'industry': info.get('industry', 'N/A'),
            'current_price': round(current_price, 2),
            'market_cap': info.get('marketCap', 'N/A'),
            'overall_score': overall,
            'technical': technical,
            'fundamental': fundamental,
            'sentiment': sentiment,
            'momentum': momentum,
            'predictions': {
                'tomorrow': short_term,
                'next_week': weekly,
                'long_term': long_term,
            },
            'entry_point': entry,
            'targets': targets,
            'metrics': metrics,
        }

    def analyze_multiple(self, symbols: List[str], timeframe: str = '1y') -> List[Dict]:
        """
        Analyze multiple stocks

        Args:
            symbols: List of stock ticker symbols
            timeframe: Data timeframe

        Returns:
            List of analysis results
        """
        results = []
        for symbol in symbols:
            result = self.analyze_stock(symbol, timeframe)
            if result:
                results.append(result)
        return results

    def rank_stocks(self, analyses: List[Dict], sort_by: str = 'overall_score') -> List[Dict]:
        """
        Rank stocks by specified criteria

        Args:
            analyses: List of stock analyses
            sort_by: Criteria to sort by

        Returns:
            Sorted list of analyses
        """
        if sort_by == 'overall_score':
            return sorted(analyses, key=lambda x: x['overall_score']['overall_score'], reverse=True)
        elif sort_by == 'momentum':
            return sorted(analyses, key=lambda x: x['momentum']['score'], reverse=True)
        elif sort_by == 'value':
            return sorted(analyses, key=lambda x: x['fundamental']['score'], reverse=True)
        elif sort_by == 'technical':
            return sorted(analyses, key=lambda x: x['technical']['score'], reverse=True)
        elif sort_by == 'sentiment':
            return sorted(analyses, key=lambda x: x['sentiment']['overall_sentiment_score'], reverse=True)
        else:
            return analyses

    def get_top_picks(self, symbols: List[str], count: int = 10, timeframe: str = '1y') -> List[Dict]:
        """
        Get top stock picks from a list

        Args:
            symbols: List of symbols to analyze
            count: Number of top picks to return
            timeframe: Data timeframe

        Returns:
            List of top picks with analysis
        """
        print(f"\nAnalyzing {len(symbols)} stocks to find top {count} picks...")
        analyses = self.analyze_multiple(symbols, timeframe)
        ranked = self.rank_stocks(analyses, 'overall_score')
        return ranked[:count]

    def get_best_value(self, symbols: List[str], count: int = 10, timeframe: str = '1y') -> List[Dict]:
        """
        Get best value stocks (high fundamental score, lower price)

        Args:
            symbols: List of symbols to analyze
            count: Number of picks to return
            timeframe: Data timeframe

        Returns:
            List of value picks
        """
        print(f"\nAnalyzing {len(symbols)} stocks for value picks...")
        analyses = self.analyze_multiple(symbols, timeframe)

        # Filter for stocks with good fundamentals
        value_picks = [a for a in analyses if a['fundamental']['score'] >= 50]

        # Sort by fundamental score
        ranked = sorted(value_picks, key=lambda x: x['fundamental']['score'], reverse=True)
        return ranked[:count]

    def get_top_gainers_prediction(self, symbols: List[str], count: int = 10, timeframe: str = '3mo') -> List[Dict]:
        """
        Predict top gainers for next day/week

        Args:
            symbols: List of symbols to analyze
            count: Number of predictions to return
            timeframe: Data timeframe

        Returns:
            List of predicted top gainers
        """
        print(f"\nAnalyzing {len(symbols)} stocks for momentum picks...")
        analyses = self.analyze_multiple(symbols, timeframe)

        # Filter for positive momentum and good score
        gainers = [a for a in analyses
                  if a['predictions']['tomorrow']['direction'] == 'Up'
                  and a['overall_score']['overall_score'] >= 50]

        # Sort by momentum and predicted change
        ranked = sorted(gainers,
                       key=lambda x: (x['momentum']['score'],
                                    x['predictions']['tomorrow']['predicted_change_pct']),
                       reverse=True)
        return ranked[:count]

    def should_buy_now(self, symbol: str) -> Dict:
        """
        Determine if a stock should be bought right now

        Args:
            symbol: Stock ticker symbol

        Returns:
            Dictionary with buy recommendation
        """
        analysis = self.analyze_stock(symbol, timeframe='6mo')
        if not analysis:
            return {'recommendation': 'Error analyzing stock'}

        score = analysis['overall_score']['overall_score']
        entry = analysis['entry_point']['entry_signal']
        sentiment = analysis['sentiment']['sentiment_rating']

        # Decision logic
        if score >= 70 and entry in ['Strong Buy Now', 'Good Entry Point']:
            recommendation = 'YES - Strong Buy'
            reason = f"High score ({score}/100) and good entry point. {sentiment} sentiment."
        elif score >= 60 and entry in ['Strong Buy Now', 'Good Entry Point', 'Consider Buying']:
            recommendation = 'YES - Buy'
            reason = f"Good score ({score}/100) and reasonable entry. {sentiment} sentiment."
        elif score >= 50 and entry in ['Strong Buy Now', 'Good Entry Point']:
            recommendation = 'MAYBE - Consider'
            reason = f"Average score ({score}/100) but good entry point. {sentiment} sentiment."
        else:
            recommendation = 'NO - Wait'
            reason = f"Score: {score}/100. {entry}. {sentiment} sentiment."

        return {
            'symbol': symbol,
            'recommendation': recommendation,
            'reason': reason,
            'score': score,
            'entry_signal': entry,
            'current_price': analysis['current_price'],
            'target_price': analysis['targets'].get('target_price', 'N/A'),
            'stop_loss': analysis['targets'].get('stop_loss', 'N/A'),
            'analysis': analysis,
        }
