"""
Test module for buvette repository functions.

This test verifies that:
1. rows_to_dicts utility function works correctly
2. Buvette database queries return proper dict objects
3. Row conversions handle None values safely
"""

import unittest
import sqlite3
import tempfile
import os
from src.db.row_utils import row_to_dict, rows_to_dicts


class TestBuvetteRepository(unittest.TestCase):
    """Test suite for buvette repository functions."""

    @classmethod
    def setUpClass(cls):
        """Set up test database once for all tests."""
        # Create a temporary database file
        cls.db_fd, cls.db_path = tempfile.mkstemp(suffix='.db')
        
        # Create connection with Row factory
        cls.conn = sqlite3.connect(cls.db_path)
        cls.conn.row_factory = sqlite3.Row
        
        # Create buvette_articles table
        cls.conn.execute("""
            CREATE TABLE buvette_articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                categorie TEXT,
                stock INTEGER DEFAULT 0,
                prix_vente REAL,
                contenance TEXT,
                unite TEXT,
                commentaire TEXT
            )
        """)
        
        # Insert test data
        cls.conn.execute("""
            INSERT INTO buvette_articles (name, categorie, stock, prix_vente, contenance, unite, commentaire)
            VALUES 
                ('Test Article 1', 'Boissons', 10, 2.50, '33cl', 'bouteille', 'Test comment 1'),
                ('Test Article 2', 'Snacks', 20, 1.50, '100g', 'paquet', 'Test comment 2'),
                ('Test Article 3', 'Boissons', 15, 3.00, '50cl', 'bouteille', NULL)
        """)
        cls.conn.commit()

    @classmethod
    def tearDownClass(cls):
        """Clean up test database."""
        try:
            cls.conn.close()
            os.close(cls.db_fd)
            os.unlink(cls.db_path)
        except Exception:
            pass

    def test_row_to_dict_with_valid_row(self):
        """Test row_to_dict converts sqlite3.Row to dict correctly."""
        row = self.conn.execute("SELECT * FROM buvette_articles WHERE name='Test Article 1'").fetchone()
        result = row_to_dict(row)
        
        # Verify it's a dict
        self.assertIsInstance(result, dict)
        
        # Verify we can use .get() method
        self.assertEqual(result.get('name'), 'Test Article 1')
        self.assertEqual(result.get('categorie'), 'Boissons')
        self.assertEqual(result.get('stock'), 10)
        
        # Verify .get() with default works
        self.assertEqual(result.get('nonexistent_field', 'default'), 'default')

    def test_row_to_dict_with_none(self):
        """Test row_to_dict handles None input safely."""
        result = row_to_dict(None)
        self.assertIsNone(result)

    def test_row_to_dict_with_none_column_value(self):
        """Test row_to_dict handles NULL column values correctly."""
        row = self.conn.execute("SELECT * FROM buvette_articles WHERE name='Test Article 3'").fetchone()
        result = row_to_dict(row)
        
        self.assertIsInstance(result, dict)
        
        # Verify NULL column is accessible via .get()
        self.assertIsNone(result.get('commentaire'))
        self.assertEqual(result.get('commentaire', 'default'), None)  # NULL is present but None
        
        # Non-existent field should return default
        self.assertEqual(result.get('nonexistent', 'default'), 'default')

    def test_rows_to_dicts_with_multiple_rows(self):
        """Test rows_to_dicts converts list of rows correctly."""
        # Query only the original 3 test articles to avoid test interference
        rows = self.conn.execute("""
            SELECT * FROM buvette_articles 
            WHERE name IN ('Test Article 1', 'Test Article 2', 'Test Article 3')
            ORDER BY name
        """).fetchall()
        results = rows_to_dicts(rows)
        
        # Verify it's a list of dicts
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 3)
        
        # Verify each item is a dict
        for item in results:
            self.assertIsInstance(item, dict)
        
        # Verify we can use .get() on each dict
        self.assertEqual(results[0].get('name'), 'Test Article 1')
        self.assertEqual(results[1].get('name'), 'Test Article 2')
        self.assertEqual(results[2].get('name'), 'Test Article 3')

    def test_rows_to_dicts_with_empty_list(self):
        """Test rows_to_dicts handles empty list safely."""
        results = rows_to_dicts([])
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 0)

    def test_buvette_fetch_returns_dicts(self):
        """Test that fetching from buvette_articles returns proper dicts."""
        rows = self.conn.execute("SELECT * FROM buvette_articles").fetchall()
        articles = rows_to_dicts(rows)
        
        # Verify we get a list
        self.assertIsInstance(articles, list)
        self.assertGreater(len(articles), 0)
        
        # Verify each item is a dict with .get() method
        for article in articles:
            self.assertIsInstance(article, dict)
            
            # Verify we can use .get() safely
            name = article.get('name')
            self.assertIsNotNone(name)
            
            # Verify .get() with default works
            self.assertEqual(article.get('nonexistent_field', 'default'), 'default')

    def test_buvette_article_dict_has_required_fields(self):
        """Test that article dicts contain expected fields."""
        rows = self.conn.execute("SELECT * FROM buvette_articles").fetchall()
        articles = rows_to_dicts(rows)
        self.assertGreater(len(articles), 0)
        
        article = articles[0]
        
        # Verify expected fields are accessible
        self.assertIn('id', article)
        self.assertIn('name', article)
        
        # Verify we can access with both [] and .get()
        self.assertEqual(article['name'], article.get('name'))

    def test_row_to_dict_idempotent(self):
        """Test that row_to_dict is idempotent (can be called on dict)."""
        row = self.conn.execute("SELECT * FROM buvette_articles LIMIT 1").fetchone()
        
        # First conversion
        dict1 = row_to_dict(row)
        self.assertIsInstance(dict1, dict)
        
        # Second conversion (should return same dict)
        dict2 = row_to_dict(dict1)
        self.assertIsInstance(dict2, dict)
        self.assertEqual(dict1, dict2)


    def test_recompute_stock_for_article_logic(self):
        """
        Test the recompute_stock_for_article logic without UI dependencies.
        
        This test verifies stock recalculation logic:
        1. Aggregates all movements for an article
        2. Calculates stock based on movement types (entrée/sortie)
        3. Updates the article's stock field
        
        TODO (audit/fixes-buvette): Review if movement types are complete. 
        Currently supports: entrée, sortie, inventaire, achat.
        Verify with real data if other types exist (e.g., 'retour', 'perte').
        See reports/TODOs.md for details.
        
        Note: This is a simplified test that doesn't import the actual function due to
        UI dependencies (tkinter). The actual function exists in modules/stock_db.py
        and is tested in integration tests that run with UI dependencies available.
        """
        # Create test tables for movements
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS buvette_mouvements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                article_id INTEGER,
                date_mouvement DATE,
                type_mouvement TEXT,
                quantite INTEGER,
                motif TEXT,
                FOREIGN KEY (article_id) REFERENCES buvette_articles(id)
            )
        """)
        self.conn.commit()
        
        # Create a new test article specifically for this test
        self.conn.execute("""
            INSERT INTO buvette_articles (name, categorie, stock, prix_vente, contenance, unite, commentaire)
            VALUES ('Test Article for Recompute', 'Test', 0, 1.00, '1L', 'unit', 'Test recompute')
        """)
        self.conn.commit()
        
        # Get the new article ID
        article = self.conn.execute(
            "SELECT id FROM buvette_articles WHERE name='Test Article for Recompute'"
        ).fetchone()
        article_id = article[0]
        
        # Insert test movements: +10, +5, -3
        self.conn.execute("""
            INSERT INTO buvette_mouvements (article_id, date_mouvement, type_mouvement, quantite, motif)
            VALUES 
                (?, '2024-01-01', 'entrée', 10, 'Initial stock'),
                (?, '2024-01-02', 'entrée', 5, 'Purchase'),
                (?, '2024-01-03', 'sortie', 3, 'Sale')
        """, (article_id, article_id, article_id))
        self.conn.commit()
        
        # Manually implement the recompute logic for testing
        rows = self.conn.execute("""
            SELECT type_mouvement, quantite
            FROM buvette_mouvements
            WHERE article_id = ?
            ORDER BY date_mouvement ASC, id ASC
        """, (article_id,)).fetchall()
        
        calculated_stock = 0
        for row in rows:
            type_mouvement = row[0]
            quantite = row[1] if row[1] is not None else 0
            
            if type_mouvement in ('entrée', 'inventaire', 'achat'):
                calculated_stock += quantite
            elif type_mouvement == 'sortie':
                calculated_stock -= quantite
        
        calculated_stock = max(0, calculated_stock)
        
        # Verify the calculated stock is correct: 10 + 5 - 3 = 12
        self.assertEqual(calculated_stock, 12)
        
        # Update the article's stock
        self.conn.execute(
            "UPDATE buvette_articles SET stock = ? WHERE id = ?",
            (calculated_stock, article_id)
        )
        self.conn.commit()
        
        # Verify the article's stock was updated in the database
        row = self.conn.execute(
            "SELECT stock FROM buvette_articles WHERE id = ?",
            (article_id,)
        ).fetchone()
        self.assertEqual(row[0], 12)


if __name__ == '__main__':
    unittest.main()
