"""
Tests for src/db/row_utils.py

This test suite validates the row_to_dict and rows_to_dicts utility functions
in the src.db.row_utils module.
"""

import unittest
import sqlite3
import tempfile
import os
from src.db.row_utils import row_to_dict, rows_to_dicts


class TestSrcRowUtils(unittest.TestCase):
    """Test suite for src.db.row_utils module."""
    
    def setUp(self):
        """Set up a temporary test database."""
        self.db_fd, self.db_path = tempfile.mkstemp()
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        
        # Create test table
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE test_table (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                optional_field TEXT,
                number_field INTEGER
            )
        """)
        
        # Insert test data
        cursor.execute(
            "INSERT INTO test_table (name, optional_field, number_field) VALUES (?, ?, ?)",
            ("Test Item 1", "Optional Value", 42)
        )
        cursor.execute(
            "INSERT INTO test_table (name, optional_field, number_field) VALUES (?, ?, ?)",
            ("Test Item 2", None, 100)
        )
        
        self.conn.commit()
    
    def tearDown(self):
        """Clean up the test database."""
        self.conn.close()
        os.close(self.db_fd)
        os.unlink(self.db_path)
    
    def test_row_to_dict_basic(self):
        """Test basic conversion of sqlite3.Row to dict."""
        cursor = self.conn.cursor()
        row = cursor.execute("SELECT * FROM test_table WHERE id=1").fetchone()
        
        # Convert to dict
        result = row_to_dict(row)
        
        # Verify it's a dict
        self.assertIsInstance(result, dict)
        
        # Verify keys and values
        self.assertEqual(result["id"], 1)
        self.assertEqual(result["name"], "Test Item 1")
        self.assertEqual(result["optional_field"], "Optional Value")
        self.assertEqual(result["number_field"], 42)
    
    def test_row_to_dict_with_get_method(self):
        """Test that converted dict supports .get() method."""
        cursor = self.conn.cursor()
        row = cursor.execute("SELECT * FROM test_table WHERE id=2").fetchone()
        
        # Convert to dict
        result = row_to_dict(row)
        
        # Test .get() with default value
        self.assertEqual(result.get("name"), "Test Item 2")
        self.assertIsNone(result.get("optional_field"))
        self.assertEqual(result.get("nonexistent_field", "default"), "default")
    
    def test_row_to_dict_with_none_input(self):
        """Test that row_to_dict returns None when input is None."""
        result = row_to_dict(None)
        self.assertIsNone(result)
    
    def test_row_to_dict_with_dict_input(self):
        """Test that row_to_dict handles dict input (idempotent)."""
        input_dict = {"id": 1, "name": "Test", "value": 42}
        result = row_to_dict(input_dict)
        
        # Should return the same dict
        self.assertEqual(result, input_dict)
    
    def test_rows_to_dicts_batch_conversion(self):
        """Test batch conversion of multiple rows."""
        cursor = self.conn.cursor()
        rows = cursor.execute("SELECT * FROM test_table ORDER BY id").fetchall()
        
        # Convert all rows
        results = rows_to_dicts(rows)
        
        # Verify count
        self.assertEqual(len(results), 2)
        
        # Verify all are dicts
        for result in results:
            self.assertIsInstance(result, dict)
        
        # Verify data
        self.assertEqual(results[0]["name"], "Test Item 1")
        self.assertEqual(results[1]["name"], "Test Item 2")
        
        # Test .get() on converted dicts
        self.assertEqual(results[0].get("optional_field"), "Optional Value")
        self.assertIsNone(results[1].get("optional_field"))
    
    def test_rows_to_dicts_empty_list(self):
        """Test rows_to_dicts with empty list."""
        result = rows_to_dicts([])
        self.assertEqual(result, [])
    
    def test_rows_to_dicts_filters_none(self):
        """Test that rows_to_dicts filters out None values."""
        cursor = self.conn.cursor()
        row1 = cursor.execute("SELECT * FROM test_table WHERE id=1").fetchone()
        row2 = cursor.execute("SELECT * FROM test_table WHERE id=2").fetchone()
        
        # Mix in a None value
        mixed_rows = [row1, None, row2]
        
        # Convert - should filter out None
        results = rows_to_dicts(mixed_rows)
        
        # Should only have 2 results
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["id"], 1)
        self.assertEqual(results[1]["id"], 2)


if __name__ == "__main__":
    unittest.main()
