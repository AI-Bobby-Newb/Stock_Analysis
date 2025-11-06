"""
Stock prediction engine
Makes predictions for different timeframes
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta


class StockPredictor:
    """Predicts stock performance for various timeframes"""

    def __init__(self):
        self.model = LinearRegression()

    def predict_short_term(self, data: pd.DataFrame, days: int = 1) -> Dict:
        """
        Predict short-term price movement (1-5 days)

        Args:
            data: DataFrame with historical price data
            days: Number of days to predict

        Returns:
            Dictionary with prediction results
        """
        if data.empty or len(data) < 30:
            return {'prediction': 'Insufficient data', 'confidence': 0}

        try:
            df = data.copy()
            current_price = df['Close'].iloc[-1]

            # Calculate technical indicators for prediction
            df['returns'] = df['Close'].pct_change()
            df['ma_5'] = df['Close'].rolling(window=5).mean()
            df['ma_20'] = df['Close'].rolling(window=20).mean()
            df['volume_ratio'] = df['Volume'] / df['Volume'].rolling(window=20).mean()

            # Use recent trend
            recent_returns = df['returns'].iloc[-10:].mean()
            volume_trend = df['volume_ratio'].iloc[-5:].mean()

            # Simple prediction based on momentum and volume
            predicted_change = recent_returns * days

            # Adjust for volume
            if volume_trend > 1.2:
                predicted_change *= 1.1
            elif volume_trend < 0.8:
                predicted_change *= 0.9

            predicted_price = current_price * (1 + predicted_change)

            # Calculate confidence based on volatility
            volatility = df['returns'].std()
            confidence = max(0, min(100, 100 - (volatility * 1000)))

            direction = 'Up' if predicted_change > 0 else 'Down'
            magnitude = abs(predicted_change * 100)

            return {
                'current_price': round(current_price, 2),
                'predicted_price': round(predicted_price, 2),
                'predicted_change_pct': round(predicted_change * 100, 2),
                'direction': direction,
                'magnitude': round(magnitude, 2),
                'confidence': round(confidence, 2),
                'timeframe': f'{days} day(s)',
            }

        except Exception as e:
            print(f"Error in short-term prediction: {e}")
            return {'prediction': 'Error', 'confidence': 0}

    def predict_medium_term(self, data: pd.DataFrame, weeks: int = 1) -> Dict:
        """
        Predict medium-term performance (1-4 weeks)

        Args:
            data: DataFrame with historical price data
            weeks: Number of weeks to predict

        Returns:
            Dictionary with prediction results
        """
        return self.predict_short_term(data, days=weeks * 7)

    def predict_long_term(self, data: pd.DataFrame, months: int = 12) -> Dict:
        """
        Predict long-term performance (3-12 months)

        Args:
            data: DataFrame with historical price data
            months: Number of months to predict

        Returns:
            Dictionary with prediction results
        """
        if data.empty or len(data) < 100:
            return {'prediction': 'Insufficient data', 'confidence': 0}

        try:
            df = data.copy()
            current_price = df['Close'].iloc[-1]

            # Use longer-term trend
            df['returns'] = df['Close'].pct_change()

            # Calculate historical growth rates
            growth_3m = ((df['Close'].iloc[-1] - df['Close'].iloc[-63]) / df['Close'].iloc[-63]) if len(df) >= 63 else 0
            growth_6m = ((df['Close'].iloc[-1] - df['Close'].iloc[-126]) / df['Close'].iloc[-126]) if len(df) >= 126 else growth_3m
            growth_12m = ((df['Close'].iloc[-1] - df['Close'].iloc[-252]) / df['Close'].iloc[-252]) if len(df) >= 252 else growth_6m

            # Weighted average of growth rates
            weights = [0.5, 0.3, 0.2]
            avg_growth = (growth_3m * weights[0] + growth_6m * weights[1] + growth_12m * weights[2])

            # Annualize and project
            annual_growth = avg_growth * (12 / 3)  # Approximate annualized rate
            predicted_growth = annual_growth * (months / 12)

            predicted_price = current_price * (1 + predicted_growth)

            # Calculate confidence based on historical consistency
            returns_std = df['returns'].std()
            confidence = max(0, min(100, 100 - (returns_std * 800)))

            # Long-term predictions are inherently less certain
            confidence *= 0.7

            direction = 'Bullish' if predicted_growth > 0 else 'Bearish'

            return {
                'current_price': round(current_price, 2),
                'predicted_price': round(predicted_price, 2),
                'predicted_change_pct': round(predicted_growth * 100, 2),
                'direction': direction,
                'confidence': round(confidence, 2),
                'timeframe': f'{months} month(s)',
                'annual_growth_rate': round(annual_growth * 100, 2),
            }

        except Exception as e:
            print(f"Error in long-term prediction: {e}")
            return {'prediction': 'Error', 'confidence': 0}

    def identify_entry_point(self, data: pd.DataFrame, score: float) -> Dict:
        """
        Identify if current price is a good entry point

        Args:
            data: DataFrame with historical price data
            score: Overall stock score

        Returns:
            Dictionary with entry point analysis
        """
        if data.empty or len(data) < 50:
            return {'entry_signal': 'Insufficient data'}

        try:
            df = data.copy()
            current_price = df['Close'].iloc[-1]

            # Calculate support/resistance levels
            high_52w = df['High'].iloc[-252:].max() if len(df) >= 252 else df['High'].max()
            low_52w = df['Low'].iloc[-252:].min() if len(df) >= 252 else df['Low'].min()

            # Position in 52-week range
            range_position = ((current_price - low_52w) / (high_52w - low_52w)) * 100

            # Moving averages
            sma_20 = df['Close'].rolling(window=20).mean().iloc[-1]
            sma_50 = df['Close'].rolling(window=50).mean().iloc[-1]

            # RSI
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            current_rsi = rsi.iloc[-1]

            # Entry signal logic
            signals = []

            if range_position < 40:
                signals.append('Near 52-week low')
            if current_price < sma_20 < sma_50 and score > 60:
                signals.append('Price below MA with good fundamentals')
            if current_rsi < 40:
                signals.append('RSI oversold')
            if current_price > sma_20 and score > 70:
                signals.append('Strong uptrend with high score')

            # Determine entry signal
            if score > 70 and len(signals) >= 2:
                entry_signal = 'Strong Buy Now'
            elif score > 60 and (current_rsi < 40 or range_position < 40):
                entry_signal = 'Good Entry Point'
            elif score > 50:
                entry_signal = 'Consider Buying'
            else:
                entry_signal = 'Wait for Better Entry'

            return {
                'entry_signal': entry_signal,
                '52w_range_position': round(range_position, 2),
                'current_vs_sma20': round(((current_price / sma_20 - 1) * 100), 2),
                'current_vs_sma50': round(((current_price / sma_50 - 1) * 100), 2),
                'rsi': round(current_rsi, 2),
                'signals': signals,
            }

        except Exception as e:
            print(f"Error identifying entry point: {e}")
            return {'entry_signal': 'Error'}

    def calculate_target_price(self, current_price: float, score: float,
                              prediction: Dict) -> Dict:
        """
        Calculate target price and stop loss

        Args:
            current_price: Current stock price
            score: Overall stock score
            prediction: Prediction results

        Returns:
            Dictionary with target and stop loss prices
        """
        try:
            # Target price based on score and prediction
            if score >= 80:
                upside = 0.25  # 25% upside
            elif score >= 65:
                upside = 0.15
            elif score >= 50:
                upside = 0.10
            else:
                upside = 0.05

            target_price = current_price * (1 + upside)

            # Stop loss (risk management)
            if score >= 70:
                stop_loss = current_price * 0.92  # 8% stop loss
            elif score >= 50:
                stop_loss = current_price * 0.90  # 10% stop loss
            else:
                stop_loss = current_price * 0.85  # 15% stop loss

            risk_reward = upside / (1 - (stop_loss / current_price))

            return {
                'target_price': round(target_price, 2),
                'stop_loss': round(stop_loss, 2),
                'upside_potential': round(upside * 100, 2),
                'downside_risk': round((1 - stop_loss / current_price) * 100, 2),
                'risk_reward_ratio': round(risk_reward, 2),
            }

        except Exception as e:
            print(f"Error calculating target price: {e}")
            return {}
