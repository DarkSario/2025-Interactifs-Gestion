"""
Central Database API Module

Provides centralized database connection management with:
- WAL mode for better concurrency
- Busy timeout to reduce lock errors
- Query helper functions (query_one, query_all)
- Transaction context manager

This module is the recommended way to interact with the database
across the application, ensuring consistent connection configuration
and error handling.
"""

import sqlite3
import time
from typing import Optional, List, Dict, Any, Callable, Tuple
from contextlib import contextmanager
from db.db import get_db_file
from utils.app_logger import get_logger
from modules.db_row_utils import _row_to_dict, _rows_to_dicts

logger = get_logger("db_api")


def get_connection(row_factory: Optional[Any] = sqlite3.Row) -> sqlite3.Connection:
    """
    Get a database connection with optimal settings.
    
    Sets:
    - PRAGMA journal_mode=WAL (Write-Ahead Logging for better concurrency)
    - PRAGMA busy_timeout=5000 (Wait up to 5 seconds if DB is locked)
    - row_factory=sqlite3.Row by default (for named column access)
    
    Args:
        row_factory: Factory for row objects (default: sqlite3.Row)
                     Set to None for tuples, or provide custom factory
    
    Returns:
        sqlite3.Connection: Configured database connection
        
    Example:
        >>> conn = get_connection()
        >>> cursor = conn.cursor()
        >>> cursor.execute("SELECT * FROM articles")
        >>> row = cursor.fetchone()
        >>> print(row['name'])  # Named access works
    """
    try:
        db_file = get_db_file()
        conn = sqlite3.connect(
            db_file, 
            timeout=10, 
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
        )
        
        # Set row factory for named column access
        if row_factory is not None:
            conn.row_factory = row_factory
        
        # Set pragmas for better concurrency and reliability
        try:
            conn.execute("PRAGMA journal_mode=WAL;")
            conn.execute("PRAGMA busy_timeout=5000;")
        except Exception as pragma_exc:
            logger.warning(f"Failed to set PRAGMAs: {pragma_exc}")
        
        return conn
    except Exception as e:
        logger.error(f"Error connecting to database: {e}")
        raise


def query_one(
    query: str, 
    params: Optional[Tuple] = None,
    converter: Optional[Callable] = None
) -> Optional[Dict[str, Any]]:
    """
    Execute a query and return a single row as a dict.
    
    Args:
        query: SQL query string
        params: Query parameters (optional)
        converter: Optional converter function (default: _row_to_dict)
                   Set to None to disable conversion
    
    Returns:
        dict or None: Single row as dict, or None if no results
        
    Example:
        >>> article = query_one("SELECT * FROM articles WHERE id = ?", (1,))
        >>> print(article.get('name', 'Unknown'))
    """
    if converter is None:
        converter = _row_to_dict
    
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        row = cursor.fetchone()
        
        if row is None:
            return None
        
        # Convert if converter provided
        if converter:
            return converter(row, cursor)
        else:
            return row
        
    except Exception as e:
        logger.error(f"Error executing query_one: {e}")
        logger.error(f"Query: {query}")
        logger.error(f"Params: {params}")
        raise
    finally:
        if conn:
            conn.close()


def query_all(
    query: str, 
    params: Optional[Tuple] = None,
    converter: Optional[Callable] = None
) -> List[Dict[str, Any]]:
    """
    Execute a query and return all rows as a list of dicts.
    
    Args:
        query: SQL query string
        params: Query parameters (optional)
        converter: Optional converter function (default: _rows_to_dicts)
                   Set to None to disable conversion
    
    Returns:
        list of dicts: All rows as dicts
        
    Example:
        >>> articles = query_all("SELECT * FROM articles WHERE categorie = ?", ('Boisson',))
        >>> for article in articles:
        >>>     print(article.get('name', 'Unknown'))
    """
    if converter is None:
        converter = _rows_to_dicts
    
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        rows = cursor.fetchall()
        
        # Convert if converter provided
        if converter:
            return converter(rows, cursor)
        else:
            return rows if rows else []
        
    except Exception as e:
        logger.error(f"Error executing query_all: {e}")
        logger.error(f"Query: {query}")
        logger.error(f"Params: {params}")
        raise
    finally:
        if conn:
            conn.close()


@contextmanager
def transaction(conn: Optional[sqlite3.Connection] = None):
    """
    Context manager for database transactions.
    
    Automatically commits on success, rolls back on exception.
    If no connection provided, creates one.
    
    Args:
        conn: Optional existing connection to use
    
    Yields:
        sqlite3.Connection: Database connection for transaction
        
    Example:
        >>> with transaction() as conn:
        >>>     cursor = conn.cursor()
        >>>     cursor.execute("INSERT INTO articles (...) VALUES (...)")
        >>>     cursor.execute("UPDATE stock SET ...")
        >>> # Automatically committed
        
        >>> # Or with existing connection:
        >>> conn = get_connection()
        >>> with transaction(conn):
        >>>     # Do multiple operations
        >>>     pass
    """
    if conn is None:
        conn = get_connection()
        close_after = True
    else:
        close_after = False
    
    try:
        yield conn
        conn.commit()
    except Exception as e:
        logger.error(f"Transaction failed, rolling back: {e}")
        conn.rollback()
        raise
    finally:
        if close_after:
            conn.close()


def execute_query(
    query: str,
    params: Optional[Tuple] = None,
    commit: bool = True
) -> int:
    """
    Execute a query (INSERT, UPDATE, DELETE) and return rows affected.
    
    Args:
        query: SQL query string
        params: Query parameters (optional)
        commit: Whether to commit the transaction (default: True)
    
    Returns:
        int: Number of rows affected
        
    Example:
        >>> rows_updated = execute_query(
        ...     "UPDATE articles SET stock = ? WHERE id = ?",
        ...     (50, 1)
        ... )
        >>> print(f"Updated {rows_updated} rows")
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        rows_affected = cursor.rowcount
        
        if commit:
            conn.commit()
        
        return rows_affected
        
    except Exception as e:
        logger.error(f"Error executing query: {e}")
        logger.error(f"Query: {query}")
        logger.error(f"Params: {params}")
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()


def execute(
    query: str,
    params: Optional[Tuple] = None,
    commit: bool = True,
    retries: int = 3,
    retry_delay: float = 0.5
) -> int:
    """
    Execute a query with retry logic for database lock errors.
    
    This function attempts to execute a query multiple times if it encounters
    a "database is locked" error, with exponential backoff between retries.
    
    Args:
        query: SQL query string (INSERT, UPDATE, DELETE)
        params: Query parameters (optional)
        commit: Whether to commit the transaction (default: True)
        retries: Number of retry attempts on lock errors (default: 3)
        retry_delay: Initial delay between retries in seconds (default: 0.5)
                     Delay doubles with each retry (exponential backoff)
    
    Returns:
        int: Number of rows affected
        
    Raises:
        sqlite3.OperationalError: If database remains locked after all retries
        Exception: Any other database error
        
    Example:
        >>> # Simple usage with default retries
        >>> rows = execute(
        ...     "UPDATE articles SET stock = ? WHERE id = ?",
        ...     (50, 1)
        ... )
        
        >>> # Custom retry configuration for critical operations
        >>> rows = execute(
        ...     "INSERT INTO orders (...) VALUES (...)",
        ...     params,
        ...     retries=5,
        ...     retry_delay=1.0
        ... )
    """
    last_exception = None
    delay = retry_delay
    
    for attempt in range(retries):
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            rows_affected = cursor.rowcount
            
            if commit:
                conn.commit()
            
            # Success - return result
            return rows_affected
            
        except sqlite3.OperationalError as e:
            last_exception = e
            error_msg = str(e).lower()
            
            # Check if this is a "database is locked" error
            if "locked" in error_msg and attempt < retries - 1:
                logger.warning(
                    f"Database locked on attempt {attempt + 1}/{retries}. "
                    f"Retrying in {delay}s... Query: {query[:100]}"
                )
                if conn:
                    try:
                        conn.close()
                    except sqlite3.Error:
                        # Ignore errors when closing connection
                        pass
                time.sleep(delay)
                delay *= 2  # Exponential backoff
                continue
            else:
                # Not a lock error or final attempt - log and raise
                logger.error(f"Database error after {attempt + 1} attempts: {e}")
                logger.error(f"Query: {query}")
                logger.error(f"Params: {params}")
                if conn:
                    try:
                        conn.rollback()
                    except sqlite3.Error:
                        # Ignore errors during rollback
                        pass
                raise
                
        except Exception as e:
            # Non-lock error - log and raise immediately
            logger.error(f"Error executing query: {e}")
            logger.error(f"Query: {query}")
            logger.error(f"Params: {params}")
            if conn:
                try:
                    conn.rollback()
                except sqlite3.Error:
                    # Ignore errors during rollback
                    pass
            raise
        finally:
            if conn:
                try:
                    conn.close()
                except sqlite3.Error:
                    # Ignore errors when closing connection
                    pass


# Convenience aliases
fetch_one = query_one
fetch_all = query_all
