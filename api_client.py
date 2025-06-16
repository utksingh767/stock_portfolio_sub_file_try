# api_client.py
"""Yahoo Finance API client for fetching stock data"""

import requests
from config import (
    YAHOO_CHART_URL, YAHOO_SEARCH_URL, USD_INR_SYMBOL,
    API_HEADERS, API_TIMEOUT, DEFAULT_USD_TO_INR_RATE
)


class YahooFinanceAPI:
    def __init__(self):
        self.usd_to_inr_rate = None
    
    def get_usd_to_inr_rate(self):
        """Get current USD to INR exchange rate"""
        try:
            if self.usd_to_inr_rate is None:
                url = YAHOO_CHART_URL.format(symbol=USD_INR_SYMBOL)
                
                response = requests.get(url, headers=API_HEADERS, timeout=API_TIMEOUT)
                data = response.json()
                
                if 'chart' in data and data['chart']['result'] and len(data['chart']['result']) > 0:
                    result = data['chart']['result'][0]
                    self.usd_to_inr_rate = result['meta']['regularMarketPrice']
                else:
                    self.usd_to_inr_rate = DEFAULT_USD_TO_INR_RATE
            
            return self.usd_to_inr_rate
        except Exception:
            return DEFAULT_USD_TO_INR_RATE
    
    def get_stock_price(self, api_symbol):
        """Get current stock price for a given symbol"""
        try:
            url = YAHOO_CHART_URL.format(symbol=api_symbol)
            
            response = requests.get(url, headers=API_HEADERS, timeout=API_TIMEOUT)
            data = response.json()
            
            if 'chart' in data and data['chart']['result'] and len(data['chart']['result']) > 0:
                result = data['chart']['result'][0]
                if 'regularMarketPrice' in result['meta']:
                    current_price = result['meta']['regularMarketPrice']
                    return current_price
                else:
                    return None
            else:
                return None
                
        except Exception as e:
            print(f"Error fetching price for {api_symbol}: {e}")
            return None
    
    def get_company_name(self, api_symbol, fallback_symbol):
        """Get company name from Yahoo Finance API"""
        try:
            url = YAHOO_SEARCH_URL.format(symbol=api_symbol)
            
            response = requests.get(url, headers=API_HEADERS, timeout=API_TIMEOUT)
            data = response.json()
            
            if 'quotes' in data and len(data['quotes']) > 0:
                return data['quotes'][0].get('longname', fallback_symbol)
            else:
                return fallback_symbol
                
        except Exception:
            return fallback_symbol