"""
Base List Dialog for Standardized Database List UIs

Provides a reusable base class for dialogs that display database records
in a Treeview widget with standardized error handling and reporting.

Features:
- load_items() helper for loading data from database with automatic conversion
- Error reporting to UTF-8 files in reports/ directory
- Graceful handling of missing columns and database errors
- Standardized logging
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Dict, Any, Optional, Tuple, Callable
from datetime import datetime
from pathlib import Path
from db.db import get_connection
from modules.db_row_utils import _rows_to_dicts
from utils.app_logger import get_logger

logger = get_logger("base_list_dialog")


class BaseListDialog:
    """
    Base class for dialogs that display database records in a Treeview.
    
    Provides standardized methods for:
    - Loading items from database with automatic row-to-dict conversion
    - Error handling and reporting
    - Graceful handling of missing columns
    
    Subclasses should:
    1. Set self.tree to their Treeview widget
    2. Call load_items() to populate the tree
    3. Override handle_load_error() for custom error handling (optional)
    """
    
    def __init__(self):
        """Initialize the base dialog."""
        self.tree = None  # Subclass should set this to their Treeview widget
        self.reports_dir = Path(__file__).parent.parent.parent / 'reports'
        self.reports_dir.mkdir(exist_ok=True)
    
    def load_items(
        self,
        tree: ttk.Treeview,
        query: str,
        params: Optional[Tuple] = None,
        columns: Optional[List[str]] = None,
        converter: Optional[Callable] = _rows_to_dicts
    ) -> bool:
        """
        Load items from database into a Treeview widget.
        
        This is the main helper method for loading database records into a tree.
        It handles:
        - Database connection
        - Query execution
        - Row-to-dict conversion (to enable .get() access)
        - Error handling and reporting
        - Graceful handling of missing columns
        
        Args:
            tree: Treeview widget to populate
            query: SQL query to execute
            params: Query parameters (optional)
            columns: List of column names to display (in order)
                    If None, will use tree's configured columns
            converter: Function to convert rows (default: _rows_to_dicts)
                      Set to None to skip conversion
        
        Returns:
            bool: True if successful, False if errors occurred
            
        Example:
            >>> self.load_items(
            ...     self.tree,
            ...     "SELECT id, name, categorie FROM articles",
            ...     columns=['id', 'name', 'categorie']
            ... )
        """
        conn = None
        try:
            # Clear existing items
            for item in tree.get_children():
                tree.delete(item)
            
            # Get connection and execute query
            conn = get_connection()
            cursor = conn.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            rows = cursor.fetchall()
            
            # Convert rows if converter provided
            if converter:
                rows = converter(rows, cursor)
            
            # Determine which columns to display
            if columns is None:
                # Use tree's configured columns
                columns = tree['columns']
            
            # Insert items into tree
            for row in rows:
                # Get ID for the tree item (try 'id' key, fall back to first value)
                if isinstance(row, dict):
                    item_id = row.get('id', '')
                    values = []
                    for col in columns:
                        value = row.get(col, '')
                        # Handle None values
                        if value is None:
                            value = ''
                        values.append(value)
                else:
                    # If not converted to dict, use positional access
                    item_id = row[0] if len(row) > 0 else ''
                    values = list(row[:len(columns)])
                
                tree.insert('', 'end', iid=item_id, values=tuple(values))
            
            return True
            
        except Exception as e:
            error_msg = f"Error loading items: {e}"
            logger.error(error_msg)
            logger.error(f"Query: {query}")
            logger.error(f"Params: {params}")
            
            # Write error report
            self._write_error_report(error_msg, query, params, e)
            
            # Handle error (can be overridden)
            self.handle_load_error(error_msg, e)
            
            return False
            
        finally:
            if conn:
                conn.close()
    
    def handle_load_error(self, error_msg: str, exception: Exception):
        """
        Handle errors during item loading.
        
        Default implementation shows a messagebox.
        Subclasses can override for custom behavior.
        
        Args:
            error_msg: Human-readable error message
            exception: The exception that was raised
        """
        messagebox.showerror(
            "Erreur de chargement",
            f"Impossible de charger les données:\n{error_msg}\n\n"
            f"Voir le fichier de rapport pour plus de détails."
        )
    
    def _write_error_report(
        self,
        error_msg: str,
        query: str,
        params: Optional[Tuple],
        exception: Exception
    ):
        """
        Write an error report to the reports directory.
        
        Creates a UTF-8 encoded file with details about the error.
        
        Args:
            error_msg: Human-readable error message
            query: SQL query that failed
            params: Query parameters
            exception: The exception that was raised
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_name = f"db_error_{timestamp}.txt"
            report_path = self.reports_dir / report_name
            
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write("Database Error Report\n")
                f.write("=" * 70 + "\n")
                f.write(f"Timestamp: {datetime.now().isoformat()}\n")
                f.write(f"Dialog: {self.__class__.__name__}\n")
                f.write("\n")
                f.write("Error:\n")
                f.write(f"{error_msg}\n")
                f.write("\n")
                f.write("Exception Type:\n")
                f.write(f"{type(exception).__name__}\n")
                f.write("\n")
                f.write("Query:\n")
                f.write(f"{query}\n")
                f.write("\n")
                f.write("Parameters:\n")
                f.write(f"{params}\n")
                f.write("\n")
                f.write("Exception Details:\n")
                f.write(f"{str(exception)}\n")
            
            logger.info(f"Error report written to {report_path}")
            
        except Exception as report_error:
            logger.error(f"Failed to write error report: {report_error}")
    
    def get_selected_id(self, tree: Optional[ttk.Treeview] = None) -> Optional[str]:
        """
        Get the ID of the selected item in the tree.
        
        Args:
            tree: Treeview widget (default: self.tree)
        
        Returns:
            str or None: ID of selected item, or None if no selection
        """
        if tree is None:
            tree = self.tree
        
        if tree is None:
            return None
        
        selection = tree.selection()
        if not selection:
            return None
        
        return selection[0]
    
    def safe_get_value(
        self,
        row: Dict[str, Any],
        key: str,
        default: Any = ''
    ) -> Any:
        """
        Safely get a value from a row dict with a default.
        
        Handles None values by converting them to the default.
        
        Args:
            row: Row dict
            key: Column name
            default: Default value if key missing or None
        
        Returns:
            Value from row, or default
        """
        value = row.get(key, default)
        if value is None:
            return default
        return value
