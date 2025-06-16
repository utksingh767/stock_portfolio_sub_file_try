# stock_utils.py
"""Utility functions for stock operations"""

from config import INDIAN_SUFFIXES, INDIAN_STOCKS


class StockUtils:
    @staticmethod
    def detect_stock_type(symbol):
        """Detect if stock is Indian or International"""
        # Check if already has Indian suffix
        if any(symbol.endswith(suffix) for suffix in INDIAN_SUFFIXES):
            return 'indian', symbol
        
        # Check against list of common Indian stocks
        if symbol.upper() in INDIAN_STOCKS:
            return 'indian', f"{symbol}.NS"
        else:
            return 'international', symbol
    
    @staticmethod
    def format_currency(amount, currency):
        """Format currency amount with appropriate symbol"""
        if currency == 'INR':
            return f"₹{amount:.2f}"
        else:
            return f"${amount:.2f}"
    
    @staticmethod
    def get_currency_symbol(currency):
        """Get currency symbol"""
        return '₹' if currency == 'INR' else '$'
    
    @staticmethod
    def get_flag_emoji(currency):
        """Get flag emoji based on currency"""
        return '🇮🇳' if currency == 'INR' else '🌍'
    
    @staticmethod
    def convert_to_inr(amount, currency, usd_to_inr_rate):
        """Convert amount to INR"""
        if currency == 'USD':
            return amount * usd_to_inr_rate
        else:
            return amount
    
    @staticmethod
    def convert_from_inr(amount_inr, target_currency, usd_to_inr_rate):
        """Convert INR amount to target currency"""
        if target_currency == 'USD':
            return amount_inr / usd_to_inr_rate
        else:
            return amount_inr