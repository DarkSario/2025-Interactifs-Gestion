#!/usr/bin/env python3
"""
Safe Column Addition Utility

This script safely adds missing columns to database tables with proper
type inference and default values.

Usage:
    python scripts/safe_add_columns.py                  # Dry-run mode
    python scripts/safe_add_columns.py --apply          # Apply changes
    python scripts/safe_add_columns.py --table TABLE    # Specific table only

Features:
    - Dry-run by default (requires --apply flag)
    - Automatic backup before changes
    - Type inference from existing columns
    - Idempotent operations (skips existing columns)
    - Transaction-safe operations
"""

import sqlite3
import argparse
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import shutil


def get_db_path() -> Path:
    """Get the database file path."""
    candidates = [
        Path("db/association.db"),
        Path("association.db"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError("Database file not found")


def backup_database(db_path: Path) -> Path:
    """
    Create a backup of the database.
    
    Returns:
        Path to backup file
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = db_path.parent / f"{db_path.stem}.bak.{timestamp}{db_path.suffix}"
    shutil.copy2(db_path, backup_path)
    return backup_path


def get_table_columns(conn: sqlite3.Connection, table: str) -> Dict[str, str]:
    """
    Get all columns and their types for a table.
    
    Returns:
        Dictionary mapping column_name -> column_type
    """
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table})")
    return {row[1]: row[2] for row in cursor.fetchall()}


def infer_column_type(column_name: str) -> str:
    """
    Infer SQL type from column name.
    
    Simple heuristics:
    - *_id, id: INTEGER
    - *_date, date, date_*: TEXT (SQLite stores dates as text)
    - montant, prix, price, quantite, quantity: REAL
    - Default: TEXT
    """
    name_lower = column_name.lower()
    
    if name_lower.endswith('_id') or name_lower == 'id':
        return 'INTEGER'
    
    if 'date' in name_lower:
        return 'TEXT'
    
    if any(word in name_lower for word in ['montant', 'prix', 'price', 'quantite', 'quantity', 'amount']):
        return 'REAL'
    
    # Default to TEXT for flexibility
    return 'TEXT'


def get_default_value(column_type: str) -> str:
    """Get appropriate default value for a column type."""
    if column_type == 'INTEGER':
        return '0'
    elif column_type == 'REAL':
        return '0.0'
    elif column_type == 'TEXT':
        return "''"
    else:
        return 'NULL'


def add_column_safe(conn: sqlite3.Connection, table: str, column: str, 
                   column_type: Optional[str] = None, 
                   default: Optional[str] = None,
                   dry_run: bool = True) -> bool:
    """
    Safely add a column to a table.
    
    Args:
        conn: Database connection
        table: Table name
        column: Column name
        column_type: SQL type (inferred if None)
        default: Default value (inferred if None)
        dry_run: If True, only simulate the operation
        
    Returns:
        True if column was added, False if it already exists
    """
    # Check if column already exists
    existing_columns = get_table_columns(conn, table)
    if column in existing_columns:
        print(f"  ✓ Column {table}.{column} already exists (type: {existing_columns[column]})")
        return False
    
    # Infer type and default if not provided
    if column_type is None:
        column_type = infer_column_type(column)
    
    if default is None:
        default = get_default_value(column_type)
    
    # Build ALTER TABLE statement
    sql = f"ALTER TABLE {table} ADD COLUMN {column} {column_type} DEFAULT {default}"
    
    if dry_run:
        print(f"  [DRY-RUN] Would execute: {sql}")
        return True
    else:
        try:
            conn.execute(sql)
            conn.commit()
            print(f"  ✓ Added column {table}.{column} ({column_type}, default={default})")
            return True
        except sqlite3.Error as e:
            print(f"  ✗ Error adding column {table}.{column}: {e}")
            return False


def add_columns_from_report(report_path: Path, conn: sqlite3.Connection, 
                           dry_run: bool = True, 
                           specific_table: Optional[str] = None) -> Tuple[int, int]:
    """
    Add columns based on missing columns report.
    
    Returns:
        Tuple of (columns_added, columns_skipped)
    """
    if not report_path.exists():
        print(f"Report file not found: {report_path}")
        return 0, 0
    
    # Parse report file to extract missing columns
    current_table = None
    missing_columns: Dict[str, List[str]] = {}
    
    content = report_path.read_text()
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('Table:'):
            current_table = line.split(':', 1)[1].strip()
            if specific_table and current_table != specific_table:
                current_table = None
                continue
            missing_columns[current_table] = []
        elif line.startswith('- ') and current_table:
            column = line[2:].strip()
            missing_columns[current_table].append(column)
    
    # Add columns
    added = 0
    skipped = 0
    
    for table, columns in missing_columns.items():
        if not columns:
            continue
            
        print(f"\nProcessing table: {table}")
        for column in columns:
            if add_column_safe(conn, table, column, dry_run=dry_run):
                added += 1
            else:
                skipped += 1
    
    return added, skipped


def add_known_columns(conn: sqlite3.Connection, dry_run: bool = True) -> Tuple[int, int]:
    """
    Add known missing columns with explicit types.
    
    Returns:
        Tuple of (columns_added, columns_skipped)
    """
    # Known missing columns with explicit types
    known_columns = [
        ('buvette_inventaire_lignes', 'commentaire', 'TEXT', "''"),
        # Add more known columns here as needed
    ]
    
    added = 0
    skipped = 0
    
    print("\nAdding known missing columns:")
    for table, column, col_type, default in known_columns:
        if add_column_safe(conn, table, column, col_type, default, dry_run):
            added += 1
        else:
            skipped += 1
    
    return added, skipped


def main():
    parser = argparse.ArgumentParser(
        description='Safely add missing columns to database tables'
    )
    parser.add_argument('--apply', action='store_true', 
                       help='Apply changes (default is dry-run)')
    parser.add_argument('--table', '-t', 
                       help='Process specific table only')
    parser.add_argument('--report', '-r', 
                       default='reports/missing_columns_report.txt',
                       help='Path to missing columns report')
    parser.add_argument('--known-only', action='store_true',
                       help='Only add known columns (ignore report)')
    args = parser.parse_args()
    
    try:
        db_path = get_db_path()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1
    
    # Mode banner
    if args.apply:
        print("=" * 70)
        print("APPLYING CHANGES TO DATABASE")
        print("=" * 70)
        print()
        
        # Create backup
        print(f"Creating backup...")
        backup_path = backup_database(db_path)
        print(f"✓ Backup created: {backup_path}")
        print()
    else:
        print("=" * 70)
        print("DRY-RUN MODE (use --apply to make changes)")
        print("=" * 70)
        print()
    
    # Connect to database
    conn = sqlite3.connect(str(db_path))
    
    try:
        # Add known columns
        added_known, skipped_known = add_known_columns(conn, dry_run=not args.apply)
        
        # Add columns from report (unless --known-only)
        added_report = 0
        skipped_report = 0
        if not args.known_only:
            report_path = Path(args.report)
            if report_path.exists():
                added_report, skipped_report = add_columns_from_report(
                    report_path, conn, 
                    dry_run=not args.apply,
                    specific_table=args.table
                )
        
        # Summary
        total_added = added_known + added_report
        total_skipped = skipped_known + skipped_report
        
        print()
        print("=" * 70)
        print("SUMMARY")
        print("=" * 70)
        print(f"Columns added:   {total_added}")
        print(f"Columns skipped: {total_skipped}")
        
        if not args.apply and total_added > 0:
            print()
            print("Note: This was a dry-run. Use --apply to make actual changes.")
        
        return 0
        
    finally:
        conn.close()


if __name__ == '__main__':
    sys.exit(main())
