"""
Test for articles unite->quantite migration backward compatibility.

This test verifies:
- Articles can be inserted and updated before migration (with 'unite')
- Migration script runs successfully
- Articles can be inserted and updated after migration (with 'unite_type')
- Data is preserved across migration
- UI functions work with both schemas
"""

import unittest
import sqlite3
import os
import sys
import tempfile
import shutil

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock tkinter before any imports that might use it
sys.modules['tkinter'] = type(sys)('tkinter')
sys.modules['tkinter.messagebox'] = type(sys)('messagebox')
sys.modules['tkinter.ttk'] = type(sys)('ttk')


def get_test_connection(db_file):
    """Create a simple connection for testing."""
    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


class TestArticlesUniteMigration(unittest.TestCase):
    """Test suite for articles unite migration compatibility."""

    def setUp(self):
        """Set up a fresh test database before each test."""
        # Create temporary file that will be auto-cleaned
        fd, self.test_db = tempfile.mkstemp(suffix='.db')
        os.close(fd)

        # Set environment variable for db.db module
        os.environ["APP_DB_PATH"] = self.test_db

        # Create the old schema (pre-migration)
        conn = get_test_connection(self.test_db)
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
        conn.commit()
        conn.close()

    def tearDown(self):
        """Clean up test database after each test."""
        try:
            if os.path.exists(self.test_db):
                os.remove(self.test_db)
            if os.path.exists(self.test_db + '.bak'):
                os.remove(self.test_db + '.bak')
        except Exception:
            pass

    def test_insert_article_pre_migration(self):
        """Test inserting article with pre-migration schema."""
        from modules.buvette_db import insert_article, list_articles

        insert_article("Test Article", "Test Cat", "bouteille", "Test comment", "1L", 2.5)

        articles = list_articles()
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0]["name"], "Test Article")
        self.assertEqual(articles[0]["unite"], "bouteille")

    def test_update_article_pre_migration(self):
        """Test updating article with pre-migration schema."""
        from modules.buvette_db import insert_article, update_article, get_article_by_id, list_articles

        insert_article("Test Article", "Test Cat", "bouteille", "Test comment", "1L", 2.5)
        
        articles = list_articles()
        article_id = articles[0]["id"]
        
        update_article(article_id, "Updated Article", "Updated Cat", "canette", "Updated comment", "0.33L", 3.0)
        
        article = get_article_by_id(article_id)
        self.assertEqual(article["name"], "Updated Article")
        self.assertEqual(article["unite"], "canette")

    def test_migration_preserves_data(self):
        """Test that migration preserves existing article data."""
        from modules.buvette_db import insert_article, list_articles, clear_schema_cache
        from scripts.migrate_articles_unite_to_quantite import migrate, backup

        # Insert test data before migration
        insert_article("Article 1", "Cat 1", "bouteille", "Comment 1", "1L", 2.5)
        insert_article("Article 2", "Cat 2", "canette", "Comment 2", "0.33L", 1.5)

        # Run migration
        backup(self.test_db)
        migrate(self.test_db)

        # Clear schema cache after migration to detect new schema
        clear_schema_cache()

        # Verify data is preserved
        articles = list_articles()
        self.assertEqual(len(articles), 2)
        
        # Check that unite was converted to unite_type
        self.assertEqual(articles[0]["unite_type"], "bouteille")
        self.assertEqual(articles[1]["unite_type"], "canette")
        
        # Check other data preserved
        self.assertEqual(articles[0]["name"], "Article 1")
        self.assertEqual(articles[1]["name"], "Article 2")

    def test_insert_article_post_migration(self):
        """Test inserting article with post-migration schema."""
        from modules.buvette_db import insert_article, list_articles, clear_schema_cache
        from scripts.migrate_articles_unite_to_quantite import migrate, backup

        # Run migration first
        backup(self.test_db)
        migrate(self.test_db)

        # Clear schema cache after migration to detect new schema
        clear_schema_cache()

        # Insert article after migration (API still uses 'unite' parameter for compatibility)
        insert_article("Test Article", "Test Cat", "bouteille", "Test comment", "1L", 2.5)

        articles = list_articles()
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0]["name"], "Test Article")
        # After migration, 'unite' is stored in 'unite_type'
        self.assertEqual(articles[0]["unite_type"], "bouteille")

    def test_update_article_post_migration(self):
        """Test updating article with post-migration schema."""
        from modules.buvette_db import insert_article, update_article, get_article_by_id, list_articles, clear_schema_cache
        from scripts.migrate_articles_unite_to_quantite import migrate, backup

        # Insert article before migration
        insert_article("Test Article", "Test Cat", "bouteille", "Test comment", "1L", 2.5)
        
        # Run migration
        backup(self.test_db)
        migrate(self.test_db)
        
        # Clear schema cache after migration to detect new schema
        clear_schema_cache()
        
        articles = list_articles()
        article_id = articles[0]["id"]
        
        # Update article after migration (API still uses 'unite' parameter for compatibility)
        update_article(article_id, "Updated Article", "Updated Cat", "canette", "Updated comment", "0.33L", 3.0)
        
        article = get_article_by_id(article_id)
        self.assertEqual(article["name"], "Updated Article")
        self.assertEqual(article["unite_type"], "canette")

    def test_stock_tab_listing_pre_migration(self):
        """Test stock_tab.get_stock_listing() with pre-migration schema."""
        from modules.buvette_db import insert_article
        from modules.stock_tab import get_stock_listing

        insert_article("Article 1", "Cat 1", "bouteille", "Comment 1", "1L", 2.5)
        insert_article("Article 2", "Cat 2", "canette", "Comment 2", "0.33L", 1.5)

        listing = get_stock_listing(scope='buvette')
        self.assertEqual(len(listing), 2)
        # Pre-migration: should have 'unite' field
        self.assertIn("unite", listing[0])

    def test_stock_tab_listing_post_migration(self):
        """Test stock_tab.get_stock_listing() with post-migration schema."""
        from modules.buvette_db import insert_article, clear_schema_cache
        from modules.stock_tab import get_stock_listing
        import modules.stock_tab
        from scripts.migrate_articles_unite_to_quantite import migrate, backup

        insert_article("Article 1", "Cat 1", "bouteille", "Comment 1", "1L", 2.5)
        
        # Run migration
        backup(self.test_db)
        migrate(self.test_db)
        
        # Clear schema cache after migration to detect new schema
        clear_schema_cache()
        modules.stock_tab.clear_schema_cache()
        
        insert_article("Article 2", "Cat 2", "canette", "Comment 2", "0.33L", 1.5)

        listing = get_stock_listing(scope='buvette')
        self.assertEqual(len(listing), 2)
        # Post-migration: should have 'unite_type' and 'quantite' fields
        self.assertIn("unite_type", listing[0])
        self.assertIn("quantite", listing[0])

    def test_migration_creates_backup(self):
        """Test that migration creates a backup file."""
        from scripts.migrate_articles_unite_to_quantite import backup

        backup(self.test_db)
        
        backup_file = self.test_db + '.bak'
        self.assertTrue(os.path.exists(backup_file))

    def test_migration_adds_columns(self):
        """Test that migration adds quantite and unite_type columns."""
        from modules.buvette_db import clear_schema_cache
        from scripts.migrate_articles_unite_to_quantite import migrate, backup

        backup(self.test_db)
        migrate(self.test_db)
        
        # Clear schema cache after migration
        clear_schema_cache()

        conn = get_test_connection(self.test_db)
        cursor = conn.execute("PRAGMA table_info(buvette_articles)")
        columns = [row[1] for row in cursor.fetchall()]
        conn.close()

        self.assertIn("quantite", columns)
        self.assertIn("unite_type", columns)
        self.assertNotIn("unite", columns)


if __name__ == '__main__':
    # Import after mocking tkinter
    from modules.buvette_db import list_articles
    unittest.main()
