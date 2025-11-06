"""
Stock scoring algorithm
Combines technical analysis, fundamental analysis, and sentiment to score stocks
"""

import pandas as pd
import numpy as np
from typing import Dict, List
import ta


class StockScorer:
    """Scores stocks based on multiple factors"""

    def __init__(self):
        self.weights = {
            'technical': 0.35,
            'fundamental': 0.35,
            'sentiment': 0.20,
            'momentum': 0.10,
        }

    def calculate_technical_score(self, data: pd.DataFrame) -> Dict:
        """
        Calculate technical analysis score

        Args:
            data: DataFrame with OHLCV data

        Returns:
            Dictionary with technical score and indicators
        """
        if data.empty or len(data) < 50:
            return {'score': 50.0, 'indicators': {}}

        try:
            df = data.copy()
            score = 0
            max_score = 0
            indicators = {}

            # RSI
            rsi = ta.momentum.RSIIndicator(df['Close'], window=14)
            current_rsi = rsi.rsi().iloc[-1]
            indicators['rsi'] = round(current_rsi, 2)

            if 30 < current_rsi < 70:
                score += 15
            elif 40 < current_rsi < 60:
                score += 20
            max_score += 20

            # MACD
            macd = ta.trend.MACD(df['Close'])
            macd_line = macd.macd().iloc[-1]
            signal_line = macd.macd_signal().iloc[-1]
            indicators['macd'] = round(macd_line, 2)
            indicators['macd_signal'] = round(signal_line, 2)

            if macd_line > signal_line:
                score += 15
            max_score += 15

            # Moving Averages
            sma_20 = df['Close'].rolling(window=20).mean().iloc[-1]
            sma_50 = df['Close'].rolling(window=50).mean().iloc[-1]
            current_price = df['Close'].iloc[-1]

            indicators['sma_20'] = round(sma_20, 2)
            indicators['sma_50'] = round(sma_50, 2)

            if current_price > sma_20 > sma_50:
                score += 25
            elif current_price > sma_20:
                score += 15
            max_score += 25

            # Bollinger Bands
            bb = ta.volatility.BollingerBands(df['Close'])
            bb_high = bb.bollinger_hband().iloc[-1]
            bb_low = bb.bollinger_lband().iloc[-1]
            bb_mid = bb.bollinger_mavg().iloc[-1]

            indicators['bb_position'] = round(((current_price - bb_low) / (bb_high - bb_low)) * 100, 2)

            if bb_low < current_price < bb_high:
                if current_price > bb_mid:
                    score += 20
                else:
                    score += 10
            max_score += 20

            # Volume
            avg_volume = df['Volume'].rolling(window=20).mean().iloc[-1]
            current_volume = df['Volume'].iloc[-1]
            indicators['volume_ratio'] = round(current_volume / avg_volume, 2)

            if current_volume > avg_volume:
                score += 10
            max_score += 10

            # ADX (Trend Strength)
            adx = ta.trend.ADXIndicator(df['High'], df['Low'], df['Close'])
            adx_value = adx.adx().iloc[-1]
            indicators['adx'] = round(adx_value, 2)

            if adx_value > 25:
                score += 10
            max_score += 10

            # Normalize score to 0-100
            final_score = (score / max_score) * 100 if max_score > 0 else 50

            return {
                'score': round(final_score, 2),
                'indicators': indicators,
            }

        except Exception as e:
            print(f"Error calculating technical score: {e}")
            return {'score': 50.0, 'indicators': {}}

    def calculate_fundamental_score(self, metrics: Dict) -> Dict:
        """
        Calculate fundamental analysis score

        Args:
            metrics: Dictionary with financial metrics

        Returns:
            Dictionary with fundamental score and analysis
        """
        if not metrics:
            return {'score': 50.0, 'analysis': {}}

        try:
            score = 0
            max_score = 0
            analysis = {}

            # P/E Ratio
            pe = metrics.get('pe_ratio')
            if pe and pe > 0:
                analysis['pe_ratio'] = pe
                if 10 < pe < 25:
                    score += 15
                elif 5 < pe < 35:
                    score += 10
                elif pe > 0:
                    score += 5
            max_score += 15

            # PEG Ratio
            peg = metrics.get('peg_ratio')
            if peg and peg > 0:
                analysis['peg_ratio'] = peg
                if peg < 1:
                    score += 15
                elif peg < 2:
                    score += 10
                elif peg < 3:
                    score += 5
            max_score += 15

            # Price to Book
            pb = metrics.get('price_to_book')
            if pb and pb > 0:
                analysis['price_to_book'] = pb
                if pb < 3:
                    score += 10
                elif pb < 5:
                    score += 5
            max_score += 10

            # Debt to Equity
            de = metrics.get('debt_to_equity')
            if de is not None:
                analysis['debt_to_equity'] = de
                if de < 0.5:
                    score += 10
                elif de < 1.0:
                    score += 7
                elif de < 2.0:
                    score += 3
            max_score += 10

            # ROE
            roe = metrics.get('roe')
            if roe:
                analysis['roe'] = round(roe * 100, 2)
                if roe > 0.15:
                    score += 15
                elif roe > 0.10:
                    score += 10
                elif roe > 0.05:
                    score += 5
            max_score += 15

            # Profit Margin
            margin = metrics.get('profit_margin')
            if margin:
                analysis['profit_margin'] = round(margin * 100, 2)
                if margin > 0.20:
                    score += 10
                elif margin > 0.10:
                    score += 7
                elif margin > 0.05:
                    score += 3
            max_score += 10

            # Revenue Growth
            rev_growth = metrics.get('revenue_growth')
            if rev_growth:
                analysis['revenue_growth'] = round(rev_growth * 100, 2)
                if rev_growth > 0.20:
                    score += 15
                elif rev_growth > 0.10:
                    score += 10
                elif rev_growth > 0.05:
                    score += 5
            max_score += 15

            # Dividend Yield
            div_yield = metrics.get('dividend_yield')
            if div_yield:
                analysis['dividend_yield'] = round(div_yield * 100, 2)
                if div_yield > 0.02:
                    score += 5
            max_score += 5

            # Beta (lower is more stable)
            beta = metrics.get('beta')
            if beta:
                analysis['beta'] = beta
                if 0.5 < beta < 1.5:
                    score += 5
            max_score += 5

            # Normalize score to 0-100
            final_score = (score / max_score) * 100 if max_score > 0 else 50

            return {
                'score': round(final_score, 2),
                'analysis': analysis,
            }

        except Exception as e:
            print(f"Error calculating fundamental score: {e}")
            return {'score': 50.0, 'analysis': {}}

    def calculate_momentum_score(self, data: pd.DataFrame) -> Dict:
        """
        Calculate momentum score based on recent price movements

        Args:
            data: DataFrame with price data

        Returns:
            Dictionary with momentum score
        """
        if data.empty or len(data) < 30:
            return {'score': 50.0, 'momentum': {}}

        try:
            df = data.copy()
            score = 0
            max_score = 0

            # 1-day return
            ret_1d = ((df['Close'].iloc[-1] - df['Close'].iloc[-2]) / df['Close'].iloc[-2]) * 100

            # 5-day return
            ret_5d = ((df['Close'].iloc[-1] - df['Close'].iloc[-6]) / df['Close'].iloc[-6]) * 100

            # 20-day return
            ret_20d = ((df['Close'].iloc[-1] - df['Close'].iloc[-21]) / df['Close'].iloc[-21]) * 100

            momentum = {
                'return_1d': round(ret_1d, 2),
                'return_5d': round(ret_5d, 2),
                'return_20d': round(ret_20d, 2),
            }

            # Score based on positive momentum
            if ret_1d > 2:
                score += 10
            elif ret_1d > 0:
                score += 5
            max_score += 10

            if ret_5d > 5:
                score += 20
            elif ret_5d > 0:
                score += 10
            max_score += 20

            if ret_20d > 10:
                score += 20
            elif ret_20d > 0:
                score += 10
            max_score += 20

            # Normalize
            final_score = (score / max_score) * 100 if max_score > 0 else 50

            return {
                'score': round(final_score, 2),
                'momentum': momentum,
            }

        except Exception as e:
            print(f"Error calculating momentum score: {e}")
            return {'score': 50.0, 'momentum': {}}

    def calculate_overall_score(self, technical: Dict, fundamental: Dict,
                               sentiment: Dict, momentum: Dict) -> Dict:
        """
        Calculate overall stock score

        Args:
            technical: Technical analysis results
            fundamental: Fundamental analysis results
            sentiment: Sentiment analysis results
            momentum: Momentum analysis results

        Returns:
            Dictionary with overall score and rating
        """
        # Extract scores
        tech_score = technical.get('score', 50.0)
        fund_score = fundamental.get('score', 50.0)
        sent_score = sentiment.get('overall_sentiment_score', 50.0)
        mom_score = momentum.get('score', 50.0)

        # Weighted average
        overall = (
            tech_score * self.weights['technical'] +
            fund_score * self.weights['fundamental'] +
            sent_score * self.weights['sentiment'] +
            mom_score * self.weights['momentum']
        )

        # Determine rating
        if overall >= 80:
            rating = 'Strong Buy'
            stars = 5
        elif overall >= 65:
            rating = 'Buy'
            stars = 4
        elif overall >= 50:
            rating = 'Hold'
            stars = 3
        elif overall >= 35:
            rating = 'Sell'
            stars = 2
        else:
            rating = 'Strong Sell'
            stars = 1

        return {
            'overall_score': round(overall, 2),
            'rating': rating,
            'stars': stars,
            'component_scores': {
                'technical': tech_score,
                'fundamental': fund_score,
                'sentiment': sent_score,
                'momentum': mom_score,
            }
        }
