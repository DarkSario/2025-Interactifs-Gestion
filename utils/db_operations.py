"""
Centralized database operations with standardized error handling and connection management.

This module provides standard patterns for database operations that:
- Ensure proper connection cleanup
- Provide consistent error handling
- Convert sqlite3.Row to dicts when needed for .get() access
- Minimize lock duration by closing connections promptly
"""

from typing import List, Dict, Any, Optional, Callable
from contextlib import contextmanager
import sqlite3

from db.db import get_connection
from utils.db_helpers import rows_to_dicts, row_to_dict
from utils.app_logger import get_logger
from utils.error_handler import handle_exception

logger = get_logger("db_operations")


@contextmanager
def db_connection():
    """
    Context manager for database connections.
    
    Ensures connections are always closed, even if an exception occurs.
    Minimizes lock duration.
    
    Usage:
        with db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM table")
            rows = cursor.fetchall()
        # Connection automatically closed here
    """
    conn = None
    try:
        conn = get_connection()
        yield conn
    finally:
        if conn:
            try:
                conn.close()
            except Exception as e:
                logger.warning(f"Error closing connection: {e}")


def execute_query(query: str, params: tuple = None, fetch: str = "all") -> List[Dict[str, Any]]:
    """
    Execute a SELECT query and return results as list of dicts.
    
    Args:
        query: SQL SELECT query
        params: Optional query parameters
        fetch: "all" to fetch all rows, "one" to fetch one row
        
    Returns:
        List of dicts (or single dict if fetch="one")
        
    Example:
        rows = execute_query("SELECT * FROM members WHERE id=?", (1,), fetch="one")
        all_members = execute_query("SELECT * FROM members ORDER BY name")
    """
    with db_connection() as conn:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if fetch == "one":
            row = cursor.fetchone()
            return row_to_dict(row) if row else None
        else:
            rows = cursor.fetchall()
            return rows_to_dicts(rows)


def _validate_table_name(table: str) -> None:
    """
    Validate table name to prevent SQL injection.
    
    Table names must contain only alphanumeric characters and underscores.
    
    Args:
        table: Table name to validate
        
    Raises:
        ValueError: If table name is invalid
    """
    import re
    if not re.match(r'^[a-zA-Z0-9_]+$', table):
        raise ValueError(f"Invalid table name: {table}. Table names must contain only alphanumeric characters and underscores.")


def execute_insert(table: str, data: Dict[str, Any]) -> int:
    """
    Execute an INSERT statement and return the new row ID.
    
    Args:
        table: Table name (validated to prevent SQL injection)
        data: Dict of column->value pairs
        
    Returns:
        ID of inserted row
        
    Raises:
        ValueError: If table name is invalid
        
    Example:
        new_id = execute_insert("members", {
            "name": "Dupont",
            "prenom": "Jean",
            "email": "jean@example.com"
        })
    """
    _validate_table_name(table)
    columns = ", ".join(data.keys())
    placeholders = ", ".join(["?" for _ in data])
    query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
    
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, tuple(data.values()))
        conn.commit()
        return cursor.lastrowid


def execute_update(table: str, data: Dict[str, Any], where: Dict[str, Any]) -> int:
    """
    Execute an UPDATE statement and return the number of affected rows.
    
    Args:
        table: Table name (validated to prevent SQL injection)
        data: Dict of column->value pairs to update
        where: Dict of column->value pairs for WHERE clause
        
    Returns:
        Number of rows updated
        
    Raises:
        ValueError: If table name is invalid
        
    Example:
        rows_updated = execute_update(
            "members",
            {"email": "new@example.com"},
            {"id": 1}
        )
    """
    _validate_table_name(table)
    set_clause = ", ".join([f"{k}=?" for k in data.keys()])
    where_clause = " AND ".join([f"{k}=?" for k in where.keys()])
    query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
    
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, tuple(data.values()) + tuple(where.values()))
        conn.commit()
        return cursor.rowcount


def execute_delete(table: str, where: Dict[str, Any]) -> int:
    """
    Execute a DELETE statement and return the number of affected rows.
    
    Args:
        table: Table name (validated to prevent SQL injection)
        where: Dict of column->value pairs for WHERE clause
        
    Returns:
        Number of rows deleted
        
    Raises:
        ValueError: If table name is invalid
        
    Example:
        rows_deleted = execute_delete("members", {"id": 1})
    """
    _validate_table_name(table)
    where_clause = " AND ".join([f"{k}=?" for k in where.keys()])
    query = f"DELETE FROM {table} WHERE {where_clause}"
    
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, tuple(where.values()))
        conn.commit()
        return cursor.rowcount


def safe_execute(operation: Callable, error_message: str = "Database operation failed") -> Optional[Any]:
    """
    Safely execute a database operation with error handling.
    
    Args:
        operation: Function to execute
        error_message: Error message to display if operation fails
        
    Returns:
        Result of operation, or None if error occurred
        
    Example:
        def fetch_members():
            return execute_query("SELECT * FROM members")
        
        members = safe_execute(fetch_members, "Failed to load members")
    """
    try:
        return operation()
    except Exception as e:
        logger.error(f"{error_message}: {e}")
        handle_exception(e, error_message)
        return None
