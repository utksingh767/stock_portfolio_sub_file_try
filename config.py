# config.py
"""Configuration and constants for the Stock Portfolio Tracker"""

# Database configuration
DATABASE_NAME = 'portfolio.db'

# API configuration
API_TIMEOUT = 10
DEFAULT_USD_TO_INR_RATE = 83.0

# Yahoo Finance API endpoints
YAHOO_CHART_URL = "https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
YAHOO_SEARCH_URL = "https://query1.finance.yahoo.com/v1/finance/search?q={symbol}"
USD_INR_SYMBOL = "USDINR=X"

# HTTP headers for API requests
API_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# Stock exchange suffixes
INDIAN_SUFFIXES = ['.NS', '.BO']

# Common Indian stock symbols (without suffix)
INDIAN_STOCKS = [
    'TCS', 'INFY', 'RELIANCE', 'HDFCBANK', 'ICICIBANK', 'ITC', 'HINDUNILVR',
    'SBIN', 'BHARTIARTL', 'KOTAKBANK', 'LT', 'ASIANPAINT', 'MARUTI', 'HCLTECH',
    'WIPRO', 'TECHM', 'TITAN', 'ULTRACEMCO', 'NESTLEIND', 'POWERGRID',
    'TATAMOTORS', 'M&M', 'ONGC', 'NTPC', 'COALINDIA', 'JSWSTEEL', 'TATASTEEL',
    'HINDALCO', 'BAJFINANCE', 'BAJAJFINSV', 'AXISBANK', 'SUNPHARMA', 'DRREDDY',
    'JIOFIN', 'JIOFINANCE', 'ADANIPORTS', 'ADANIENT', 'DIVISLAB', 'BRITANNIA',
    'CIPLA', 'EICHERMOT', 'GRASIM', 'HDFCLIFE', 'HEROMOTOCO', 'INDUSINDBK',
    'LICI', 'SHRIRAMFIN', 'TATACONSUM', 'VEDL', 'APOLLOHOSP', 'BAJAJ-AUTO',
    'BPCL', 'IOC', 'SHREECEM', 'UPL', 'ZYDUSLIFE'
]

# Display formatting
DISPLAY_WIDTH = 95
SHORT_DISPLAY_WIDTH = 75