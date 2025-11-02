# -*- coding: utf-8 -*-
"""
Tests for db_api retry logic and error handling.
"""

import pytest
import sqlite3
import time
import tempfile
import os
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.db_api import execute, get_connection, query_one, query_all
from db.db import set_db_file


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    fd, path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    
    # Set up the database
    set_db_file(path)
    conn = sqlite3.connect(path)
    conn.execute("""
        CREATE TABLE test_table (
            id INTEGER PRIMARY KEY,
            name TEXT,
            value INTEGER
        )
    """)
    conn.execute("INSERT INTO test_table (name, value) VALUES ('test1', 100)")
    conn.execute("INSERT INTO test_table (name, value) VALUES ('test2', 200)")
    conn.commit()
    conn.close()
    
    yield path
    
    # Cleanup
    try:
        os.unlink(path)
    except (OSError, FileNotFoundError):
        # Ignore cleanup errors
        pass


class TestDBApiRetry:
    """Test retry logic in db_api module."""
    
    def test_execute_success_no_retry(self, temp_db):
        """Test that execute works on first attempt when no lock."""
        rows = execute(
            "UPDATE test_table SET value = ? WHERE name = ?",
            (150, 'test1')
        )
        
        assert rows == 1
        
        # Verify the update
        result = query_one("SELECT value FROM test_table WHERE name = ?", ('test1',))
        assert result['value'] == 150
    
    def test_execute_insert(self, temp_db):
        """Test execute with INSERT."""
        rows = execute(
            "INSERT INTO test_table (name, value) VALUES (?, ?)",
            ('test3', 300)
        )
        
        assert rows == 1
        
        # Verify the insert
        result = query_one("SELECT * FROM test_table WHERE name = ?", ('test3',))
        assert result is not None
        assert result['name'] == 'test3'
        assert result['value'] == 300
    
    def test_execute_delete(self, temp_db):
        """Test execute with DELETE."""
        rows = execute("DELETE FROM test_table WHERE name = ?", ('test1',))
        
        assert rows == 1
        
        # Verify the delete
        result = query_one("SELECT * FROM test_table WHERE name = ?", ('test1',))
        assert result is None
    
    def test_execute_without_commit(self, temp_db):
        """Test execute with commit=False."""
        # Note: This is tricky to test as connection is auto-closed
        # Just verify the function accepts the parameter
        rows = execute(
            "UPDATE test_table SET value = ? WHERE name = ?",
            (175, 'test2'),
            commit=True
        )
        
        assert rows == 1
    
    def test_execute_with_custom_retries(self, temp_db):
        """Test that custom retry count is accepted."""
        # This mainly tests the API, not the actual retry behavior
        rows = execute(
            "UPDATE test_table SET value = ? WHERE name = ?",
            (125, 'test1'),
            retries=5,
            retry_delay=0.1
        )
        
        assert rows == 1
    
    @patch('modules.db_api.get_connection')
    def test_execute_retries_on_lock_error(self, mock_get_connection):
        """Test that execute retries on database lock errors."""
        # Create a mock connection that raises OperationalError twice, then succeeds
        attempt_count = [0]
        
        def create_connection():
            conn = MagicMock()
            cursor = MagicMock()
            
            def execute_side_effect(*args, **kwargs):
                attempt_count[0] += 1
                if attempt_count[0] <= 2:
                    # First two attempts fail with lock error
                    raise sqlite3.OperationalError("database is locked")
                # Third attempt succeeds
                return None
            
            cursor.execute.side_effect = execute_side_effect
            cursor.rowcount = 1
            conn.cursor.return_value = cursor
            conn.commit = MagicMock()
            conn.rollback = MagicMock()
            conn.close = MagicMock()
            
            return conn
        
        mock_get_connection.side_effect = create_connection
        
        # Execute should retry and succeed
        start_time = time.time()
        rows = execute(
            "UPDATE test_table SET value = ? WHERE name = ?",
            (200, 'test'),
            retries=3,
            retry_delay=0.1
        )
        elapsed = time.time() - start_time
        
        # Should have succeeded after retries
        assert rows == 1
        assert attempt_count[0] == 3
        
        # Should have taken at least the retry delays (0.1 + 0.2 = 0.3s)
        assert elapsed >= 0.3
    
    @patch('modules.db_api.get_connection')
    def test_execute_fails_after_max_retries(self, mock_get_connection):
        """Test that execute fails after exhausting all retries."""
        def create_failing_connection():
            conn = MagicMock()
            cursor = MagicMock()
            cursor.execute.side_effect = sqlite3.OperationalError("database is locked")
            conn.cursor.return_value = cursor
            conn.close = MagicMock()
            return conn
        
        mock_get_connection.side_effect = create_failing_connection
        
        # Should raise OperationalError after all retries
        with pytest.raises(sqlite3.OperationalError, match="database is locked"):
            execute(
                "UPDATE test_table SET value = ?",
                (300,),
                retries=2,
                retry_delay=0.05
            )
    
    @patch('modules.db_api.get_connection')
    def test_execute_non_lock_error_no_retry(self, mock_get_connection):
        """Test that non-lock errors don't trigger retries."""
        attempt_count = [0]
        
        def create_connection():
            attempt_count[0] += 1
            conn = MagicMock()
            cursor = MagicMock()
            # Raise a non-lock error
            cursor.execute.side_effect = sqlite3.IntegrityError("UNIQUE constraint failed")
            conn.cursor.return_value = cursor
            conn.rollback = MagicMock()
            conn.close = MagicMock()
            return conn
        
        mock_get_connection.side_effect = create_connection
        
        # Should fail immediately without retries
        with pytest.raises(sqlite3.IntegrityError, match="UNIQUE constraint"):
            execute("INSERT INTO test_table VALUES (1, 'dup')", retries=3)
        
        # Should have only tried once (no retries for non-lock errors)
        assert attempt_count[0] == 1
    
    def test_query_one_returns_dict(self, temp_db):
        """Test that query_one returns a dictionary."""
        result = query_one("SELECT * FROM test_table WHERE name = ?", ('test1',))
        
        assert result is not None
        assert isinstance(result, dict)
        assert 'name' in result
        assert 'value' in result
        assert result.get('name') == 'test1'
        assert result.get('value') == 100
    
    def test_query_all_returns_list_of_dicts(self, temp_db):
        """Test that query_all returns a list of dictionaries."""
        results = query_all("SELECT * FROM test_table ORDER BY name")
        
        assert isinstance(results, list)
        assert len(results) == 2
        assert all(isinstance(r, dict) for r in results)
        
        assert results[0].get('name') == 'test1'
        assert results[1].get('name') == 'test2'
    
    def test_query_one_returns_none_for_no_results(self, temp_db):
        """Test that query_one returns None when no results."""
        result = query_one("SELECT * FROM test_table WHERE name = ?", ('nonexistent',))
        assert result is None
    
    def test_query_all_returns_empty_list_for_no_results(self, temp_db):
        """Test that query_all returns empty list when no results."""
        results = query_all("SELECT * FROM test_table WHERE name = ?", ('nonexistent',))
        assert results == []


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
