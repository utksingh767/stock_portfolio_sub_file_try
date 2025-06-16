# main.py
"""Main application entry point for the Global Stock Portfolio Tracker"""

from portfolio_manager import PortfolioManager
from display_utils import DisplayUtils
from stock_utils import StockUtils


def main():
    """Main application loop"""
    portfolio = PortfolioManager()
    display = DisplayUtils()
    utils = StockUtils()
    
    while True:
        display.show_main_menu()
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '1':
            portfolio.view_portfolio()
        
        elif choice == '2':
            try:
                display.show_add_stock_help()
                
                symbol = input("\nEnter stock symbol: ").strip().upper()
                if not symbol:
                    print("❌ Please enter a valid symbol")
                    continue
                
                stock_type, _ = utils.detect_stock_type(symbol)
                currency = 'INR' if stock_type == 'indian' else 'USD'
                currency_symbol = utils.get_currency_symbol(currency)
                flag = utils.get_flag_emoji(currency)
                
                print(f"{flag} Detected as {stock_type.title()} stock ({currency})")
                
                quantity = int(input("Enter quantity: "))
                buy_price = float(input(f"Enter buy price per share: {currency_symbol}"))
                
                portfolio.add_stock(symbol, quantity, buy_price)
                
            except ValueError:
                print("❌ Please enter valid numbers for quantity and price")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        elif choice == '3':
            if portfolio.list_stocks_with_ids():
                try:
                    stock_id = int(input("\nEnter ID of stock to delete: "))
                    portfolio.delete_stock(stock_id)
                except ValueError:
                    print("❌ Please enter a valid ID number")
        
        elif choice == '4':
            portfolio.delete_multiple_stocks()
        
        elif choice == '5':
            portfolio.get_portfolio_stats()
        
        elif choice == '6':
            print("👋 Thanks for using Global Stock Portfolio Tracker!")
            break
        
        else:
            print("❌ Invalid choice. Please enter 1-6.")


if __name__ == "__main__":
    main()