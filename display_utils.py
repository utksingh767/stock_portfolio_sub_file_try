# display_utils.py
"""Display utilities for formatting portfolio output"""

from config import DISPLAY_WIDTH, SHORT_DISPLAY_WIDTH
from stock_utils import StockUtils


class DisplayUtils:
    def __init__(self):
        self.utils = StockUtils()
    
    def show_portfolio_header(self, usd_to_inr_rate):
        """Display portfolio header"""
        print("\n" + "="*DISPLAY_WIDTH)
        print("📊 YOUR GLOBAL STOCK PORTFOLIO")
        print(f"💱 USD to INR Rate: {usd_to_inr_rate:.2f}")
        print("="*DISPLAY_WIDTH)
        print(f"{'Flag':<4} {'Symbol':<10} {'Company':<18} {'Qty':<5} {'Buy Price':<12} {'Current':<12} {'Value':<14} {'P&L':<14}")
        print("-"*DISPLAY_WIDTH)
    
    def show_stock_row(self, symbol, company, quantity, buy_price, currency, 
                      current_price, price_currency, current_value_inr, invested_inr):
        """Display a single stock row with current price"""
        flag = self.utils.get_flag_emoji(currency)
        buy_price_display = self.utils.format_currency(buy_price, currency)
        current_price_display = self.utils.format_currency(current_price, price_currency)
        value_display = f"₹{current_value_inr:,.2f}"
        
        pnl_inr = current_value_inr - invested_inr
        pnl_color = "🟢" if pnl_inr >= 0 else "🔴"
        
        print(f"{flag:<4} {symbol:<10} {company[:17]:<18} {quantity:<5} {buy_price_display:<12} {current_price_display:<12} {value_display:<14} {pnl_color}₹{pnl_inr:>11.2f}")
    
    def show_stock_row_no_price(self, symbol, company, quantity, buy_price, currency):
        """Display a single stock row when price is unavailable"""
        flag = self.utils.get_flag_emoji(currency)
        buy_price_display = self.utils.format_currency(buy_price, currency)
        
        print(f"{flag:<4} {symbol:<10} {company[:17]:<18} {quantity:<5} {buy_price_display:<12} {'N/A':<12} {'N/A':<14} {'N/A':<14}")
    
    def show_portfolio_totals(self, total_invested_inr, total_current_inr, usd_to_inr_rate):
        """Display portfolio totals"""
        print("-"*DISPLAY_WIDTH)
        
        total_pnl_inr = total_current_inr - total_invested_inr
        total_pnl_percent = (total_pnl_inr / total_invested_inr) * 100 if total_invested_inr > 0 else 0
        pnl_emoji = "🟢" if total_pnl_inr >= 0 else "🔴"
        
        print(f"💰 Total Invested: ₹{total_invested_inr:,.2f} (${total_invested_inr/usd_to_inr_rate:,.2f})")
        print(f"📈 Current Value:  ₹{total_current_inr:,.2f} (${total_current_inr/usd_to_inr_rate:,.2f})")
        print(f"{pnl_emoji} Total P&L:     ₹{total_pnl_inr:,.2f} ({total_pnl_percent:+.2f}%)")
        print("="*DISPLAY_WIDTH)
    
    def show_stocks_list_for_deletion(self, stocks):
        """Display stocks list with IDs for deletion purposes"""
        print("\n📋 Your Stocks (for deletion):")
        print(f"{'ID':<4} {'Flag':<4} {'Symbol':<10} {'Company':<20} {'Quantity':<8} {'Buy Price':<12} {'Date Added':<12}")
        print("-"*SHORT_DISPLAY_WIDTH)
        
        for stock in stocks:
            # Handle both old and new database schema
            if len(stock) == 6:  # Old schema
                id, symbol, company, quantity, buy_price, date_added = stock
                stock_type, _ = StockUtils.detect_stock_type(symbol)
                currency = 'INR' if stock_type == 'indian' else 'USD'
            else:  # New schema
                id, symbol, company, quantity, buy_price, date_added, currency = stock
            
            flag = self.utils.get_flag_emoji(currency)
            buy_price_display = self.utils.format_currency(buy_price, currency)
            date_short = date_added.split()[0] if ' ' in date_added else date_added[:10]
            
            print(f"{id:<4} {flag:<4} {symbol:<10} {company[:19]:<20} {quantity:<8} {buy_price_display:<12} {date_short:<12}")
    
    def show_main_menu(self):
        """Display main menu"""
        print("\n🌍 GLOBAL STOCK PORTFOLIO TRACKER")
        print("1. 📊 View Portfolio")
        print("2. ➕ Add Stock (Indian/International)")
        print("3. 🗑️ Delete Single Stock")
        print("4. 🗑️ Delete Multiple Stocks")
        print("5. 📈 Portfolio Stats")
        print("6. 🚪 Exit")
    
    def show_add_stock_help(self):
        """Display help for adding stocks"""
        print("\n📈 Add New Stock:")
        print("🇮🇳 Indian stocks: TCS, INFY, RELIANCE, HDFCBANK, ITC")
        print("🌍 International: AAPL, GOOGL, TSLA, MSFT, NVDA")