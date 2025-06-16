# portfolio_manager.py
"""Core portfolio management functionality"""

from database_manager import DatabaseManager
from api_client import YahooFinanceAPI
from stock_utils import StockUtils
from display_utils import DisplayUtils


class PortfolioManager:
    def __init__(self):
        self.db = DatabaseManager()
        self.api = YahooFinanceAPI()
        self.utils = StockUtils()
        self.display = DisplayUtils()
    
    def add_stock(self, symbol, quantity, buy_price):
        """Add a stock to portfolio"""
        symbol = symbol.upper()
        stock_type, api_symbol = self.utils.detect_stock_type(symbol)
        
        # Get company name from API
        company_name = self.api.get_company_name(api_symbol, symbol)
        
        # Determine currency
        currency = 'INR' if stock_type == 'indian' else 'USD'
        
        # Add to database
        self.db.add_stock(symbol, company_name, quantity, buy_price, currency)
        
        # Display confirmation
        currency_symbol = self.utils.get_currency_symbol(currency)
        flag = self.utils.get_flag_emoji(currency)
        print(f"✅ {flag} Added {quantity} shares of {symbol} at {currency_symbol}{buy_price:.2f} each ({currency})")
    
    def view_portfolio(self):
        """Display current portfolio with live prices"""
        stocks = self.db.get_all_stocks()
        
        if not stocks:
            print("📈 Your portfolio is empty. Add some stocks first!")
            return
        
        # Get exchange rate
        usd_to_inr = self.api.get_usd_to_inr_rate()
        
        # Display portfolio
        self.display.show_portfolio_header(usd_to_inr)
        
        total_invested_inr = 0
        total_current_inr = 0
        
        for stock in stocks:
            # Handle both old and new database schema
            if len(stock) == 6:  # Old schema without currency
                id, symbol, company, quantity, buy_price, date_added = stock
                stock_type, _ = self.utils.detect_stock_type(symbol)
                currency = 'INR' if stock_type == 'indian' else 'USD'
            else:  # New schema with currency
                id, symbol, company, quantity, buy_price, date_added, currency = stock
            
            # Get current price
            stock_type, api_symbol = self.utils.detect_stock_type(symbol)
            current_price = self.api.get_stock_price(api_symbol)
            price_currency = 'INR' if stock_type == 'indian' else 'USD'
            
            if current_price:
                # Calculate values in INR for totals
                invested_inr = self.utils.convert_to_inr(quantity * buy_price, currency, usd_to_inr)
                current_value_inr = self.utils.convert_to_inr(quantity * current_price, price_currency, usd_to_inr)
                
                total_invested_inr += invested_inr
                total_current_inr += current_value_inr
                
                # Display stock row
                self.display.show_stock_row(
                    symbol, company, quantity, buy_price, currency,
                    current_price, price_currency, current_value_inr, invested_inr
                )
            else:
                self.display.show_stock_row_no_price(symbol, company, quantity, buy_price, currency)
        
        # Display totals
        self.display.show_portfolio_totals(total_invested_inr, total_current_inr, usd_to_inr)
    
    def delete_stock(self, stock_id):
        """Delete a single stock from portfolio"""
        success, result = self.db.delete_stock(stock_id)
        
        if success:
            symbol, company, quantity = result
            print(f"🗑️ Successfully deleted {quantity} shares of {symbol} ({company}) from portfolio")
        else:
            print("❌ Stock not found with that ID")
    
    def list_stocks_with_ids(self):
        """List all stocks with their IDs for deletion"""
        stocks = self.db.get_all_stocks()
        
        if not stocks:
            print("📈 Your portfolio is empty.")
            return False
        
        self.display.show_stocks_list_for_deletion(stocks)
        return True
    
    def delete_multiple_stocks(self):
        """Delete multiple stocks by ID"""
        if not self.list_stocks_with_ids():
            return
        
        print("\n🗑️ Delete Multiple Stocks")
        print("Enter stock IDs to delete (comma-separated, e.g., 1,3,5)")
        print("Or type 'cancel' to go back")
        
        ids_input = input("\nEnter IDs: ").strip()
        
        if ids_input.lower() == 'cancel':
            print("❌ Operation cancelled.")
            return
        
        try:
            # Parse and validate IDs
            stock_ids = [int(id.strip()) for id in ids_input.split(',') if id.strip()]
            
            if not stock_ids:
                print("❌ No valid IDs entered.")
                return
            
            # Get details of stocks to be deleted
            stocks_to_delete = self.db.get_stocks_by_id(stock_ids)
            
            if not stocks_to_delete:
                print("❌ No stocks found with the provided IDs.")
                return
            
            # Show confirmation
            print(f"\n📋 Found {len(stocks_to_delete)} stock(s) to delete:")
            for id, symbol, company, quantity in stocks_to_delete:
                print(f"  • ID {id}: {symbol} ({company}) - {quantity} shares")
            
            confirm = input(f"\nConfirm deletion of {len(stocks_to_delete)} stock(s)? (y/n): ").strip().lower()
            
            if confirm == 'y':
                deleted_count = self.db.delete_multiple_stocks(stock_ids)
                print(f"🗑️ Successfully deleted {deleted_count} stock(s) from portfolio!")
            else:
                print("❌ Deletion cancelled.")
            
        except ValueError:
            print("❌ Please enter valid numeric IDs separated by commas.")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def get_portfolio_stats(self):
        """Get and display portfolio statistics"""
        stats, total_count = self.db.get_portfolio_stats()
        
        print(f"\n📊 Portfolio Statistics:")
        print("-" * 30)
        
        if total_count == 0:
            print("📈 Portfolio is empty")
        else:
            print(f"📈 Total Stocks: {total_count}")
            for count, currency in stats:
                flag = self.utils.get_flag_emoji(currency)
                print(f"  {flag} {currency} stocks: {count}")