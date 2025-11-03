"""
Tests pour le système de journal de stock.

Ce fichier teste:
- La création de la table inventory_stock_journal
- L'application d'un snapshot d'inventaire
- L'annulation des effets d'un inventaire
- La récupération de l'historique du journal
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


class TestStockJournal(unittest.TestCase):
    """Test suite for stock journal management."""

    def setUp(self):
        """Set up a fresh test database before each test."""
        # Create temporary file that will be auto-cleaned
        fd, self.test_db = tempfile.mkstemp(suffix='.db')
        os.close(fd)

        # Set environment variable for db.db module
        os.environ["APP_DB_PATH"] = self.test_db

        # Create the tables
        conn = get_test_connection(self.test_db)

        # Create events table (needed for FK)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                date TEXT,
                lieu TEXT,
                description TEXT
            )
        """)

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

        # Create buvette_inventaires table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS buvette_inventaires (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date_inventaire DATE,
                event_id INTEGER,
                type_inventaire TEXT CHECK(type_inventaire IN
                    ('avant', 'apres', 'hors_evenement')),
                commentaire TEXT,
                FOREIGN KEY (event_id) REFERENCES events(id)
            )
        """)

        # Create buvette_inventaire_lignes table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS buvette_inventaire_lignes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                inventaire_id INTEGER,
                article_id INTEGER,
                quantite INTEGER,
                commentaire TEXT,
                FOREIGN KEY (inventaire_id)
                    REFERENCES buvette_inventaires(id),
                FOREIGN KEY (article_id) REFERENCES buvette_articles(id)
            )
        """)

        conn.commit()
        conn.close()

    def tearDown(self):
        """Clean up test database after each test."""
        try:
            if os.path.exists(self.test_db):
                os.remove(self.test_db)
        except Exception:
            pass

    def test_ensure_stock_tables(self):
        """Test that ensure_stock_tables creates the journal table."""
        from modules.stock_db import ensure_stock_tables

        conn = get_test_connection(self.test_db)
        ensure_stock_tables(conn)
        conn.commit()

        cursor = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' "
            "AND name='inventory_stock_journal'"
        )
        result = cursor.fetchone()
        conn.close()

        self.assertIsNotNone(result, "inventory_stock_journal table should exist")

    def test_get_set_stock(self):
        """Test getting and setting stock for an article."""
        from modules.stock_db import get_stock, set_stock

        conn = get_test_connection(self.test_db)
        cursor = conn.execute(
            "INSERT INTO buvette_articles (name, stock) VALUES (?, ?)",
            ("Test Article", 0)
        )
        article_id = cursor.lastrowid
        conn.commit()

        # Test get_stock
        stock = get_stock(conn, article_id)
        self.assertEqual(stock, 0, "Initial stock should be 0")

        # Test set_stock
        set_stock(conn, article_id, 10)
        conn.commit()
        stock = get_stock(conn, article_id)
        self.assertEqual(stock, 10, "Stock should be updated to 10")
        
        conn.close()

    def test_apply_inventory_snapshot(self):
        """Test applying an inventory snapshot updates stock and journal."""
        from modules.stock_db import (
            ensure_stock_tables, apply_inventory_snapshot, get_stock
        )

        conn = get_test_connection(self.test_db)
        ensure_stock_tables(conn)

        # Create test articles with initial stock
        cursor = conn.execute(
            "INSERT INTO buvette_articles (name, stock) VALUES (?, ?)",
            ("Article 1", 5)
        )
        article1_id = cursor.lastrowid
        cursor = conn.execute(
            "INSERT INTO buvette_articles (name, stock) VALUES (?, ?)",
            ("Article 2", 10)
        )
        article2_id = cursor.lastrowid

        # Create test inventory
        cursor = conn.execute(
            "INSERT INTO buvette_inventaires "
            "(date_inventaire, type_inventaire) VALUES (?, ?)",
            ("2024-01-01", "hors_evenement")
        )
        inv_id = cursor.lastrowid

        # Create inventory lines
        conn.execute(
            "INSERT INTO buvette_inventaire_lignes "
            "(inventaire_id, article_id, quantite) VALUES (?, ?, ?)",
            (inv_id, article1_id, 8)
        )
        conn.execute(
            "INSERT INTO buvette_inventaire_lignes "
            "(inventaire_id, article_id, quantite) VALUES (?, ?, ?)",
            (inv_id, article2_id, 7)
        )

        conn.commit()

        # Apply snapshot
        apply_inventory_snapshot(conn, inv_id)
        conn.commit()

        # Check that stock was updated
        self.assertEqual(
            get_stock(conn, article1_id), 8,
            "Article 1 stock should be updated to 8"
        )
        self.assertEqual(
            get_stock(conn, article2_id), 7,
            "Article 2 stock should be updated to 7"
        )

        # Check that journal entries were created
        rows = conn.execute("""
            SELECT article_id, delta FROM inventory_stock_journal
            WHERE inventaire_id=?
            ORDER BY article_id
        """, (inv_id,)).fetchall()

        self.assertEqual(len(rows), 2, "Should have 2 journal entries")
        self.assertEqual(rows[0]["article_id"], article1_id)
        self.assertEqual(
            rows[0]["delta"], 3, "Article 1 delta should be +3 (8-5)"
        )
        self.assertEqual(rows[1]["article_id"], article2_id)
        self.assertEqual(
            rows[1]["delta"], -3, "Article 2 delta should be -3 (7-10)"
        )
        
        conn.close()

    def test_revert_inventory_effect(self):
        """Test reverting inventory effects restores stock."""
        from modules.stock_db import (
            ensure_stock_tables, apply_inventory_snapshot,
            revert_inventory_effect, get_stock
        )

        conn = get_test_connection(self.test_db)
        ensure_stock_tables(conn)

        # Create test articles with initial stock
        cursor = conn.execute(
            "INSERT INTO buvette_articles (name, stock) VALUES (?, ?)",
            ("Article 1", 5)
        )
        article1_id = cursor.lastrowid
        cursor = conn.execute(
            "INSERT INTO buvette_articles (name, stock) VALUES (?, ?)",
            ("Article 2", 10)
        )
        article2_id = cursor.lastrowid

        # Create test inventory
        cursor = conn.execute(
            "INSERT INTO buvette_inventaires "
            "(date_inventaire, type_inventaire) VALUES (?, ?)",
            ("2024-01-01", "hors_evenement")
        )
        inv_id = cursor.lastrowid

        # Create inventory lines
        conn.execute(
            "INSERT INTO buvette_inventaire_lignes "
            "(inventaire_id, article_id, quantite) VALUES (?, ?, ?)",
            (inv_id, article1_id, 8)
        )
        conn.execute(
            "INSERT INTO buvette_inventaire_lignes "
            "(inventaire_id, article_id, quantite) VALUES (?, ?, ?)",
            (inv_id, article2_id, 7)
        )

        conn.commit()

        # Apply snapshot
        apply_inventory_snapshot(conn, inv_id)
        conn.commit()

        # Verify stock was updated
        self.assertEqual(get_stock(conn, article1_id), 8)
        self.assertEqual(get_stock(conn, article2_id), 7)

        # Revert the inventory
        revert_inventory_effect(conn, inv_id)
        conn.commit()

        # Check that stock was restored
        self.assertEqual(
            get_stock(conn, article1_id), 5,
            "Article 1 stock should be restored to 5"
        )
        self.assertEqual(
            get_stock(conn, article2_id), 10,
            "Article 2 stock should be restored to 10"
        )

        # Check that journal entries were deleted
        rows = conn.execute("""
            SELECT COUNT(*) as count FROM inventory_stock_journal
            WHERE inventaire_id=?
        """, (inv_id,)).fetchone()

        self.assertEqual(
            rows["count"], 0,
            "Journal entries should be deleted after revert"
        )
        
        conn.close()

    def test_inventory_stock_journal(self):
        """Test retrieving stock journal for an inventory."""
        from modules.stock_db import (
            ensure_stock_tables, apply_inventory_snapshot,
            inventory_stock_journal
        )

        conn = get_test_connection(self.test_db)
        ensure_stock_tables(conn)

        # Create test article
        cursor = conn.execute(
            "INSERT INTO buvette_articles (name, stock) VALUES (?, ?)",
            ("Test Article", 5)
        )
        article_id = cursor.lastrowid

        # Create test inventory
        cursor = conn.execute(
            "INSERT INTO buvette_inventaires "
            "(date_inventaire, type_inventaire) VALUES (?, ?)",
            ("2024-01-01", "hors_evenement")
        )
        inv_id = cursor.lastrowid

        # Create inventory line
        conn.execute(
            "INSERT INTO buvette_inventaire_lignes "
            "(inventaire_id, article_id, quantite) VALUES (?, ?, ?)",
            (inv_id, article_id, 12)
        )

        conn.commit()

        # Apply snapshot
        apply_inventory_snapshot(conn, inv_id)
        conn.commit()

        # Get journal
        journal = inventory_stock_journal(conn, inv_id)

        self.assertEqual(len(journal), 1, "Should have 1 journal entry")
        self.assertEqual(journal[0]["article_id"], article_id)
        self.assertEqual(journal[0]["delta"], 7, "Delta should be +7 (12-5)")
        self.assertEqual(journal[0]["article_name"], "Test Article")
        
        conn.close()


if __name__ == '__main__':
    unittest.main()
