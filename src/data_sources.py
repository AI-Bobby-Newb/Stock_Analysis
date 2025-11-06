"""
Free data sources for stock analysis
Uses Yahoo Finance (via yfinance) as primary source
"""

import yfinance as yf
import pandas as pd
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import time


class StockDataSource:
    """Handles fetching stock data from free sources"""

    def __init__(self):
        self.cache = {}
        self.cache_timeout = 300  # 5 minutes

    def get_stock_data(self, symbol: str, period: str = "1y") -> Optional[pd.DataFrame]:
        """
        Fetch stock data using yfinance

        Args:
            symbol: Stock ticker symbol
            period: Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)

        Returns:
            DataFrame with stock data or None if error
        """
        cache_key = f"{symbol}_{period}"

        # Check cache
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if time.time() - timestamp < self.cache_timeout:
                return cached_data

        try:
            stock = yf.Ticker(symbol)
            df = stock.history(period=period)

            if not df.empty:
                self.cache[cache_key] = (df, time.time())
                return df
            return None
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            return None

    def get_stock_info(self, symbol: str) -> Dict:
        """
        Get stock info/fundamentals

        Args:
            symbol: Stock ticker symbol

        Returns:
            Dictionary with stock information
        """
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            return info
        except Exception as e:
            print(f"Error fetching info for {symbol}: {e}")
            return {}

    def get_current_price(self, symbol: str) -> Optional[float]:
        """Get current stock price"""
        try:
            stock = yf.Ticker(symbol)
            data = stock.history(period="1d")
            if not data.empty:
                return data['Close'].iloc[-1]
            return None
        except Exception as e:
            print(f"Error fetching price for {symbol}: {e}")
            return None

    def get_multiple_stocks(self, symbols: List[str], period: str = "1y") -> Dict[str, pd.DataFrame]:
        """
        Fetch data for multiple stocks

        Args:
            symbols: List of stock ticker symbols
            period: Time period

        Returns:
            Dictionary mapping symbol to DataFrame
        """
        result = {}
        for symbol in symbols:
            data = self.get_stock_data(symbol, period)
            if data is not None:
                result[symbol] = data
        return result

    def get_trending_tickers(self) -> List[str]:
        """
        Get trending tickers (using a predefined list of popular stocks)
        In production, this could scrape from financial websites
        """
        # Popular stocks across sectors
        trending = [
            # Tech
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA', 'TSLA', 'AMD', 'INTC', 'CRM',
            # Finance
            'JPM', 'BAC', 'WFC', 'GS', 'MS', 'V', 'MA', 'PYPL',
            # Healthcare
            'JNJ', 'UNH', 'PFE', 'ABBV', 'TMO', 'MRK',
            # Consumer
            'WMT', 'HD', 'DIS', 'NKE', 'SBUX', 'MCD', 'COST',
            # Energy
            'XOM', 'CVX', 'COP',
            # Industrial
            'BA', 'CAT', 'GE',
        ]
        return trending

    def get_tech_stocks(self) -> List[str]:
        """Get list of major tech stocks"""
        return [
            'AAPL', 'MSFT', 'GOOGL', 'GOOG', 'AMZN', 'META', 'NVDA', 'TSLA',
            'AMD', 'INTC', 'CRM', 'ADBE', 'NFLX', 'ORCL', 'CSCO', 'AVGO',
            'QCOM', 'TXN', 'AMAT', 'MU', 'SNOW', 'PLTR', 'COIN'
        ]

    def get_financial_metrics(self, symbol: str) -> Dict:
        """
        Calculate key financial metrics

        Args:
            symbol: Stock ticker symbol

        Returns:
            Dictionary with financial metrics
        """
        try:
            stock = yf.Ticker(symbol)
            info = stock.info

            metrics = {
                'pe_ratio': info.get('trailingPE', None),
                'forward_pe': info.get('forwardPE', None),
                'peg_ratio': info.get('pegRatio', None),
                'price_to_book': info.get('priceToBook', None),
                'price_to_sales': info.get('priceToSalesTrailing12Months', None),
                'debt_to_equity': info.get('debtToEquity', None),
                'current_ratio': info.get('currentRatio', None),
                'roe': info.get('returnOnEquity', None),
                'roa': info.get('returnOnAssets', None),
                'profit_margin': info.get('profitMargins', None),
                'operating_margin': info.get('operatingMargins', None),
                'market_cap': info.get('marketCap', None),
                'enterprise_value': info.get('enterpriseValue', None),
                'beta': info.get('beta', None),
                'dividend_yield': info.get('dividendYield', None),
                '52_week_high': info.get('fiftyTwoWeekHigh', None),
                '52_week_low': info.get('fiftyTwoWeekLow', None),
                'avg_volume': info.get('averageVolume', None),
                'revenue_growth': info.get('revenueGrowth', None),
                'earnings_growth': info.get('earningsGrowth', None),
            }

            return metrics
        except Exception as e:
            print(f"Error getting metrics for {symbol}: {e}")
            return {}
