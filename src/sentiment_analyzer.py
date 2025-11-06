"""
Sentiment analysis for stock predictions
Uses free sources: stock news, social media signals, and market sentiment
"""

import yfinance as yf
import requests
from textblob import TextBlob
from typing import Dict, List, Tuple
from datetime import datetime, timedelta
import pandas as pd


class SentimentAnalyzer:
    """Analyzes sentiment from various free sources"""

    def __init__(self):
        self.sentiment_cache = {}

    def analyze_text(self, text: str) -> Tuple[float, float]:
        """
        Analyze sentiment of text using TextBlob

        Args:
            text: Text to analyze

        Returns:
            Tuple of (polarity, subjectivity)
            polarity: -1 (negative) to 1 (positive)
            subjectivity: 0 (objective) to 1 (subjective)
        """
        try:
            blob = TextBlob(text)
            return blob.sentiment.polarity, blob.sentiment.subjectivity
        except Exception as e:
            print(f"Error analyzing text: {e}")
            return 0.0, 0.0

    def get_stock_news_sentiment(self, symbol: str) -> Dict:
        """
        Get sentiment from stock news

        Args:
            symbol: Stock ticker symbol

        Returns:
            Dictionary with sentiment analysis
        """
        try:
            stock = yf.Ticker(symbol)
            news = stock.news

            if not news:
                return {
                    'sentiment_score': 0.0,
                    'news_count': 0,
                    'positive_count': 0,
                    'negative_count': 0,
                    'neutral_count': 0,
                    'average_polarity': 0.0,
                }

            sentiments = []
            positive = 0
            negative = 0
            neutral = 0

            for article in news[:20]:  # Analyze recent 20 articles
                title = article.get('title', '')
                summary = article.get('summary', '')
                text = f"{title}. {summary}"

                polarity, subjectivity = self.analyze_text(text)
                sentiments.append(polarity)

                if polarity > 0.1:
                    positive += 1
                elif polarity < -0.1:
                    negative += 1
                else:
                    neutral += 1

            avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0.0

            # Calculate overall sentiment score (0-100)
            sentiment_score = ((avg_sentiment + 1) / 2) * 100

            return {
                'sentiment_score': round(sentiment_score, 2),
                'news_count': len(news),
                'positive_count': positive,
                'negative_count': negative,
                'neutral_count': neutral,
                'average_polarity': round(avg_sentiment, 3),
            }

        except Exception as e:
            print(f"Error getting news sentiment for {symbol}: {e}")
            return {
                'sentiment_score': 50.0,
                'news_count': 0,
                'positive_count': 0,
                'negative_count': 0,
                'neutral_count': 0,
                'average_polarity': 0.0,
            }

    def get_market_sentiment_indicators(self, symbol: str, data: pd.DataFrame) -> Dict:
        """
        Calculate market sentiment indicators from price/volume data

        Args:
            symbol: Stock ticker symbol
            data: DataFrame with stock data

        Returns:
            Dictionary with market sentiment indicators
        """
        try:
            if data.empty or len(data) < 20:
                return {'market_sentiment': 50.0, 'volume_trend': 'neutral'}

            # Price momentum
            recent_return = ((data['Close'].iloc[-1] - data['Close'].iloc[-20]) /
                           data['Close'].iloc[-20]) * 100

            # Volume trend
            recent_volume = data['Volume'].iloc[-5:].mean()
            historical_volume = data['Volume'].iloc[-30:-5].mean()
            volume_ratio = recent_volume / historical_volume if historical_volume > 0 else 1.0

            # Volatility
            returns = data['Close'].pct_change()
            volatility = returns.std() * (252 ** 0.5) * 100  # Annualized

            # Price trend
            sma_20 = data['Close'].rolling(window=20).mean().iloc[-1]
            sma_50 = data['Close'].rolling(window=50).mean().iloc[-1] if len(data) >= 50 else sma_20
            current_price = data['Close'].iloc[-1]

            # Calculate sentiment score
            sentiment = 50  # neutral base

            # Price momentum component
            if recent_return > 10:
                sentiment += 20
            elif recent_return > 5:
                sentiment += 10
            elif recent_return > 0:
                sentiment += 5
            elif recent_return < -10:
                sentiment -= 20
            elif recent_return < -5:
                sentiment -= 10
            elif recent_return < 0:
                sentiment -= 5

            # Volume component
            if volume_ratio > 1.5:
                sentiment += 10
            elif volume_ratio > 1.2:
                sentiment += 5
            elif volume_ratio < 0.8:
                sentiment -= 5

            # Trend component
            if current_price > sma_20 > sma_50:
                sentiment += 10
            elif current_price < sma_20 < sma_50:
                sentiment -= 10

            sentiment = max(0, min(100, sentiment))

            volume_trend = 'increasing' if volume_ratio > 1.2 else 'decreasing' if volume_ratio < 0.8 else 'neutral'

            return {
                'market_sentiment': round(sentiment, 2),
                'volume_trend': volume_trend,
                'volume_ratio': round(volume_ratio, 2),
                'recent_return': round(recent_return, 2),
                'volatility': round(volatility, 2),
                'price_vs_sma20': round(((current_price / sma_20 - 1) * 100), 2),
            }

        except Exception as e:
            print(f"Error calculating market sentiment for {symbol}: {e}")
            return {'market_sentiment': 50.0, 'volume_trend': 'neutral'}

    def get_overall_sentiment(self, symbol: str, data: pd.DataFrame) -> Dict:
        """
        Get overall sentiment combining news and market indicators

        Args:
            symbol: Stock ticker symbol
            data: DataFrame with stock data

        Returns:
            Dictionary with overall sentiment analysis
        """
        news_sentiment = self.get_stock_news_sentiment(symbol)
        market_sentiment = self.get_market_sentiment_indicators(symbol, data)

        # Weighted average: 40% news, 60% market indicators
        overall_score = (news_sentiment['sentiment_score'] * 0.4 +
                        market_sentiment['market_sentiment'] * 0.6)

        # Determine overall rating
        if overall_score >= 75:
            rating = 'Very Bullish'
        elif overall_score >= 60:
            rating = 'Bullish'
        elif overall_score >= 40:
            rating = 'Neutral'
        elif overall_score >= 25:
            rating = 'Bearish'
        else:
            rating = 'Very Bearish'

        return {
            'overall_sentiment_score': round(overall_score, 2),
            'sentiment_rating': rating,
            'news_sentiment': news_sentiment,
            'market_sentiment': market_sentiment,
        }
