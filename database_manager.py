# database_manager.py
"""Database operations for the Stock Portfolio Tracker"""

import sqlite3
from datetime import datetime
from config import DATABASE_NAME


class DatabaseManager:
    def __init__(self, db_name=DATABASE_NAME):
        self.db_name = db_name
        self.init_db()
    
    def init_db(self):
        """Initialize SQLite database with proper schema"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Create table with old schema first
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stocks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                company_name TEXT,
                quantity INTEGER NOT NULL,
                buy_price REAL NOT NULL,
                date_added TEXT NOT NULL
            )
        ''')
        
        # Check if currency column exists, if not add it
        cursor.execute("PRAGMA table_info(stocks)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'currency' not in columns:
            print("🔄 Updating database schema...")
            cursor.execute('ALTER TABLE stocks ADD COLUMN currency TEXT')
            
            # Update existing records with currency based on stock type
            from stock_utils import StockUtils
            stock_utils = StockUtils()
            
            cursor.execute('SELECT id, symbol FROM stocks WHERE currency IS NULL')
            stocks_to_update = cursor.fetchall()
            
            for stock_id, symbol in stocks_to_update:
                stock_type, _ = stock_utils.detect_stock_type(symbol)
                currency = 'INR' if stock_type == 'indian' else 'USD'
                cursor.execute('UPDATE stocks SET currency = ? WHERE id = ?', (currency, stock_id))
            
            print("✅ Database schema updated successfully!")
        
        conn.commit()
        conn.close()
    
    def add_stock(self, symbol, company_name, quantity, buy_price, currency):
        """Add a stock to the database"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO stocks (symbol, company_name, quantity, buy_price, currency, date_added)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (symbol, company_name, quantity, buy_price, currency, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        
        conn.commit()
        conn.close()
    
    def get_all_stocks(self):
        """Get all stocks from database"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM stocks ORDER BY date_added DESC')
        stocks = cursor.fetchall()
        conn.close()
        
        return stocks
    
    def get_stocks_by_id(self, stock_ids):
        """Get specific stocks by their IDs"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        placeholders = ','.join(['?' for _ in stock_ids])
        cursor.execute(f'SELECT id, symbol, company_name, quantity FROM stocks WHERE id IN ({placeholders})', stock_ids)
        stocks = cursor.fetchall()
        conn.close()
        
        return stocks
    
    def delete_stock(self, stock_id):
        """Delete a single stock by ID"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('SELECT symbol, company_name, quantity FROM stocks WHERE id = ?', (stock_id,))
        result = cursor.fetchone()
        
        if result:
            symbol, company, quantity = result
            cursor.execute('DELETE FROM stocks WHERE id = ?', (stock_id,))
            conn.commit()
            conn.close()
            return True, (symbol, company, quantity)
        else:
            conn.close()
            return False, None
    
    def delete_multiple_stocks(self, stock_ids):
        """Delete multiple stocks by IDs"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        placeholders = ','.join(['?' for _ in stock_ids])
        cursor.execute(f'DELETE FROM stocks WHERE id IN ({placeholders})', stock_ids)
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        return deleted_count
    
    def get_portfolio_stats(self):
        """Get portfolio statistics"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*), currency FROM stocks GROUP BY currency')
        stats = cursor.fetchall()
        
        cursor.execute('SELECT COUNT(*) FROM stocks')
        total_count = cursor.fetchone()[0]
        
        conn.close()
        
        return stats, total_count