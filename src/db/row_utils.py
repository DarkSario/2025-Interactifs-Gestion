"""
Database row utility functions for safe sqlite3.Row conversions.

This module provides utility functions to safely convert sqlite3.Row objects
to dictionaries, enabling the use of .get() method for optional field access.

sqlite3.Row objects support dictionary-style access (row['column']) but
lack the .get() method that dicts have for optional fields with defaults.
This causes AttributeError when code tries to use row.get('column', default).

Functions:
    row_to_dict: Convert a single sqlite3.Row to dict
    rows_to_dicts: Convert a list of sqlite3.Row objects to list of dicts

Example:
    >>> from src.db.connection import connect
    >>> from src.db.row_utils import row_to_dict
    >>> 
    >>> conn = connect()
    >>> cursor = conn.cursor()
    >>> row = cursor.execute("SELECT * FROM table").fetchone()
    >>> row_dict = row_to_dict(row)
    >>> value = row_dict.get('optional_column', 'default')
"""

import sqlite3
from typing import Any, Dict, List, Optional


def row_to_dict(row: Optional[sqlite3.Row]) -> Optional[Dict[str, Any]]:
    """
    Convert sqlite3.Row to dict for safe .get() access.
    
    sqlite3.Row objects support dictionary-style access (row['column']) but
    lack the .get() method that dicts have for optional fields with defaults.
    This function converts a Row to a dict to enable .get() usage.
    
    Args:
        row: sqlite3.Row object or None
        
    Returns:
        dict or None: Dictionary representation of the row, or None if input is None
        
    Example:
        >>> row = cursor.execute("SELECT * FROM table").fetchone()
        >>> row_dict = row_to_dict(row)
        >>> value = row_dict.get('optional_column', 'default')
        
    Note:
        - Returns None if input is None
        - Returns the dict unchanged if input is already a dict (idempotent)
        - Handles sqlite3.Row objects by converting to dict
    """
    if row is None:
        return None
    
    # If already a dict, return as-is (idempotent operation)
    if isinstance(row, dict):
        return row
    
    # Convert sqlite3.Row to dict
    # sqlite3.Row supports dict() conversion via keys() method
    try:
        return dict(row)
    except (TypeError, ValueError) as e:
        # Fallback for unexpected types
        raise TypeError(f"Cannot convert {type(row)} to dict: {e}")


def rows_to_dicts(rows: List[Any]) -> List[Dict[str, Any]]:
    """
    Convert list of sqlite3.Row objects to list of dicts.
    
    This is a batch version of row_to_dict() for converting multiple rows.
    Filters out None values automatically.
    
    Args:
        rows: list of sqlite3.Row objects
        
    Returns:
        list of dicts: List of dictionary representations
        
    Example:
        >>> rows = cursor.execute("SELECT * FROM table").fetchall()
        >>> dicts = rows_to_dicts(rows)
        >>> for d in dicts:
        >>>     print(d.get('optional_column', 'N/A'))
        
    Note:
        - Returns empty list if input is empty
        - Automatically filters out None values
        - Each row is converted via row_to_dict()
    """
    if not rows:
        return []
    
    result = []
    for row in rows:
        converted = row_to_dict(row)
        if converted is not None:
            result.append(converted)
    
    return result
