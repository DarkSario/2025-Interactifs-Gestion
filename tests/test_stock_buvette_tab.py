"""
Tests for Stock Buvette tab integration.

This file tests:
- get_stock_listing function from stock_tab module
- Stock display in Buvette UI context
- Integration with buvette_articles table
"""

import unittest
import sqlite3
import os
import sys
import tempfile

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock tkinter before any imports that might use it
sys.modules['tkinter'] = type(sys)('tkinter')
sys.modules['tkinter.messagebox'] = type(sys)('messagebox')


def get_test_connection(db_file):
    """Create a simple connection for testing."""
    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


class TestStockBuvetteTab(unittest.TestCase):
    """Test suite for Stock Buvette tab functionality."""

    def setUp(self):
        """Set up a fresh test database before each test."""
        # Create temporary file that will be auto-cleaned
        tmp_file = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        self.test_db = tmp_file.name
        tmp_file.close()

        # Set environment variable for db.db module
        os.environ["APP_DB_PATH"] = self.test_db

        # Create the tables
        conn = get_test_connection(self.test_db)

        # Create buvette_articles table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS buvette_articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                categorie TEXT,
                unite TEXT,
                contenance TEXT,
                commentaire TEXT,
                stock INTEGER DEFAULT 0,
                purchase_price REAL
            )
        """)

        # Insert test data
        test_articles = [
            ('Coca Cola', 'Boissons', 'bouteille', '0.33L', 'Stock test', 10, 1.5),
            ('Chips', 'Snacks', 'paquet', '100g', 'En stock', 25, 2.0),
            ('Eau', 'Boissons', 'bouteille', '1L', '', 50, 0.5),
            ('Sandwich', 'Repas', 'unité', '', 'Fait maison', 5, 3.5),
        ]
        
        for article in test_articles:
            conn.execute("""
                INSERT INTO buvette_articles 
                (name, categorie, unite, contenance, commentaire, stock, purchase_price)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, article)

        conn.commit()
        conn.close()

    def tearDown(self):
        """Clean up test database after each test."""
        try:
            if os.path.exists(self.test_db):
                os.remove(self.test_db)
        except Exception:
            pass

    def test_get_stock_listing_returns_all_articles(self):
        """Test that get_stock_listing returns all articles with stock info."""
        from modules.stock_tab import get_stock_listing

        stock_list = get_stock_listing(scope='buvette')

        # Should return 4 articles
        self.assertEqual(len(stock_list), 4, "Should return all 4 articles")

        # Check that all expected fields are present
        expected_fields = ['id', 'name', 'categorie', 'stock', 'unite', 
                          'contenance', 'commentaire']
        for item in stock_list:
            for field in expected_fields:
                self.assertIn(field, item, f"Field {field} should be present")

    def test_get_stock_listing_includes_stock_values(self):
        """Test that stock values are correctly included."""
        from modules.stock_tab import get_stock_listing

        stock_list = get_stock_listing(scope='buvette')

        # Find specific articles and check stock
        coca = next((a for a in stock_list if a['name'] == 'Coca Cola'), None)
        self.assertIsNotNone(coca, "Coca Cola should be in stock list")
        self.assertEqual(coca['stock'], 10, "Coca Cola stock should be 10")

        eau = next((a for a in stock_list if a['name'] == 'Eau'), None)
        self.assertIsNotNone(eau, "Eau should be in stock list")
        self.assertEqual(eau['stock'], 50, "Eau stock should be 50")

    def test_get_stock_listing_sorted_by_name(self):
        """Test that articles are sorted by name."""
        from modules.stock_tab import get_stock_listing

        stock_list = get_stock_listing(scope='buvette')

        names = [item['name'] for item in stock_list]
        sorted_names = sorted(names)
        
        self.assertEqual(names, sorted_names, 
                        "Articles should be sorted alphabetically by name")

    def test_get_stock_listing_with_empty_database(self):
        """Test that empty database returns empty list."""
        from modules.stock_tab import get_stock_listing

        # Clear the database
        conn = get_test_connection(self.test_db)
        conn.execute("DELETE FROM buvette_articles")
        conn.commit()
        conn.close()

        stock_list = get_stock_listing(scope='buvette')

        self.assertEqual(len(stock_list), 0, 
                        "Empty database should return empty list")

    def test_get_stock_listing_handles_null_values(self):
        """Test that null values are handled gracefully."""
        from modules.stock_tab import get_stock_listing

        # Add article with null values
        conn = get_test_connection(self.test_db)
        conn.execute("""
            INSERT INTO buvette_articles 
            (name, categorie, unite, contenance, commentaire, stock)
            VALUES (?, ?, ?, ?, ?, ?)
        """, ('Test Article', None, None, None, None, None))
        conn.commit()
        conn.close()

        stock_list = get_stock_listing(scope='buvette')

        # Should include the new article
        test_article = next((a for a in stock_list 
                            if a['name'] == 'Test Article'), None)
        self.assertIsNotNone(test_article, 
                            "Article with null values should be included")

    def test_get_stock_listing_scope_validation(self):
        """Test that only buvette scope is supported."""
        from modules.stock_tab import get_stock_listing

        # Test with valid scope
        stock_list = get_stock_listing(scope='buvette')
        self.assertIsInstance(stock_list, list, 
                             "Should return list for valid scope")

        # Test with invalid scope
        stock_list_invalid = get_stock_listing(scope='invalid')
        self.assertEqual(len(stock_list_invalid), 0,
                        "Invalid scope should return empty list")

    def test_stock_listing_integration_with_stock_updates(self):
        """Test that stock listing reflects stock updates."""
        from modules.stock_tab import get_stock_listing

        # Get initial stock
        stock_list = get_stock_listing(scope='buvette')
        coca = next((a for a in stock_list if a['name'] == 'Coca Cola'), None)
        initial_stock = coca['stock']

        # Update stock
        conn = get_test_connection(self.test_db)
        conn.execute(
            "UPDATE buvette_articles SET stock=? WHERE name=?",
            (initial_stock + 5, 'Coca Cola')
        )
        conn.commit()
        conn.close()

        # Get updated stock list
        updated_stock_list = get_stock_listing(scope='buvette')
        updated_coca = next((a for a in updated_stock_list 
                            if a['name'] == 'Coca Cola'), None)

        self.assertEqual(updated_coca['stock'], initial_stock + 5,
                        "Stock list should reflect updated stock values")


if __name__ == '__main__':
    unittest.main()
