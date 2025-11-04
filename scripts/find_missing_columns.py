#!/usr/bin/env python3
"""
Database Schema Auditor - Find Missing Columns

This script audits the SQLite database schema to detect missing columns
referenced in code but not present in database tables.

Usage:
    python scripts/find_missing_columns.py                # Generate report
    python scripts/find_missing_columns.py --verbose      # Show detailed output
    python scripts/find_missing_columns.py --table TABLE  # Check specific table

Output:
    - reports/missing_columns_report.txt
    - Console summary of findings
"""

import sqlite3
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple
import argparse
import ast
import re


def get_db_path():
    """Get the database file path."""
    # Try common locations
    candidates = [
        Path("db/association.db"),
        Path("association.db"),
        Path("../db/association.db"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    # Return default even if doesn't exist (will be created)
    return Path("db/association.db")


def get_table_columns(db_path: Path) -> Dict[str, Set[str]]:
    """
    Extract all table names and their columns from the database.
    
    Returns:
        Dictionary mapping table_name -> set of column names
    """
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    tables = [row[0] for row in cursor.fetchall()]
    
    # Get columns for each table
    schema = {}
    for table in tables:
        cursor.execute(f"PRAGMA table_info({table})")
        columns = {row[1] for row in cursor.fetchall()}  # row[1] is column name
        schema[table] = columns
    
    conn.close()
    return schema


def scan_code_for_column_references(root_dir: Path) -> Dict[str, Set[str]]:
    """
    Scan Python code for SQL column references.
    
    Returns:
        Dictionary mapping table_name -> set of referenced column names
    """
    references = {}
    
    # Patterns to detect column references in SQL queries
    # This is a simplified approach - can be enhanced
    select_pattern = re.compile(r'SELECT\s+(.+?)\s+FROM\s+(\w+)', re.IGNORECASE | re.DOTALL)
    insert_pattern = re.compile(r'INSERT\s+INTO\s+(\w+)\s*\(([^)]+)\)', re.IGNORECASE)
    update_pattern = re.compile(r'UPDATE\s+(\w+)\s+SET\s+(.+?)(?:WHERE|$)', re.IGNORECASE | re.DOTALL)
    where_pattern = re.compile(r'WHERE\s+(.+?)(?:ORDER|GROUP|LIMIT|$)', re.IGNORECASE | re.DOTALL)
    
    # Scan all Python files
    for py_file in root_dir.rglob('*.py'):
        # Skip test files, migrations, and virtual environments
        if any(skip in str(py_file) for skip in ['test', 'venv', '.venv', '__pycache__', 'migration']):
            continue
            
        try:
            content = py_file.read_text(encoding='utf-8', errors='ignore')
            
            # Find SELECT statements
            for match in select_pattern.finditer(content):
                columns_str, table_name = match.groups()
                if table_name not in references:
                    references[table_name] = set()
                    
                # Parse column names (simplified - doesn't handle all SQL syntax)
                if columns_str.strip() != '*':
                    cols = [c.strip().split()[-1].split('.')[-1] 
                           for c in columns_str.split(',')]
                    references[table_name].update(cols)
            
            # Find INSERT statements
            for match in insert_pattern.finditer(content):
                table_name, columns_str = match.groups()
                if table_name not in references:
                    references[table_name] = set()
                cols = [c.strip() for c in columns_str.split(',')]
                references[table_name].update(cols)
            
            # Find UPDATE statements
            for match in update_pattern.finditer(content):
                table_name, set_clause = match.groups()
                if table_name not in references:
                    references[table_name] = set()
                # Extract column names from SET clause
                cols = [c.split('=')[0].strip() for c in set_clause.split(',')]
                references[table_name].update(cols)
                
        except Exception as e:
            # Silently skip files that can't be read
            pass
    
    return references


def find_missing_columns(db_path: Path, root_dir: Path) -> Dict[str, Set[str]]:
    """
    Find columns referenced in code but missing from database tables.
    
    Returns:
        Dictionary mapping table_name -> set of missing column names
    """
    db_schema = get_table_columns(db_path)
    code_refs = scan_code_for_column_references(root_dir)
    
    missing = {}
    for table, referenced_cols in code_refs.items():
        if table not in db_schema:
            # Table doesn't exist - might be intentional or a bigger issue
            continue
        
        actual_cols = db_schema[table]
        missing_cols = referenced_cols - actual_cols
        
        # Filter out common SQL keywords and functions that aren't columns
        sql_keywords = {'AS', 'FROM', 'WHERE', 'ORDER', 'BY', 'GROUP', 'HAVING', 
                       'LIMIT', 'OFFSET', 'JOIN', 'ON', 'AND', 'OR', 'NOT', 'IN',
                       'LIKE', 'BETWEEN', 'IS', 'NULL', 'COUNT', 'SUM', 'AVG', 
                       'MAX', 'MIN', 'DISTINCT', 'CASE', 'WHEN', 'THEN', 'ELSE', 'END'}
        missing_cols = {col for col in missing_cols 
                       if col.upper() not in sql_keywords 
                       and not col.startswith('?')
                       and len(col) > 0}
        
        if missing_cols:
            missing[table] = missing_cols
    
    return missing


def check_known_missing_columns(db_schema: Dict[str, Set[str]]) -> Dict[str, Set[str]]:
    """
    Check for known missing columns that are frequently referenced in the codebase.
    
    Returns:
        Dictionary mapping table_name -> set of known missing columns
    """
    known_issues = {}
    
    # Known issue: buvette_inventaire_lignes.commentaire
    if 'buvette_inventaire_lignes' in db_schema:
        if 'commentaire' not in db_schema['buvette_inventaire_lignes']:
            known_issues['buvette_inventaire_lignes'] = {'commentaire'}
    
    # Add other known issues here as they're discovered
    
    return known_issues


def generate_report(missing: Dict[str, Set[str]], known_issues: Dict[str, Set[str]], 
                   output_file: Path, verbose: bool = False):
    """Generate a detailed report of missing columns."""
    
    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append("DATABASE SCHEMA AUDIT REPORT - Missing Columns")
    report_lines.append("=" * 80)
    report_lines.append("")
    report_lines.append(f"Generated: {Path.cwd()}")
    report_lines.append("")
    
    # Summary
    total_tables = len(missing) + len(known_issues)
    total_columns = sum(len(cols) for cols in missing.values()) + sum(len(cols) for cols in known_issues.values())
    
    if total_tables == 0:
        report_lines.append("✓ No missing columns detected!")
        report_lines.append("")
    else:
        report_lines.append(f"⚠ Found missing columns in {total_tables} table(s)")
        report_lines.append(f"⚠ Total missing columns: {total_columns}")
        report_lines.append("")
    
    # Known issues
    if known_issues:
        report_lines.append("-" * 80)
        report_lines.append("KNOWN MISSING COLUMNS (High Priority)")
        report_lines.append("-" * 80)
        report_lines.append("")
        
        for table, columns in sorted(known_issues.items()):
            report_lines.append(f"Table: {table}")
            for col in sorted(columns):
                report_lines.append(f"  - {col}")
            report_lines.append("")
    
    # Detected missing columns
    if missing:
        report_lines.append("-" * 80)
        report_lines.append("DETECTED MISSING COLUMNS (From Code Analysis)")
        report_lines.append("-" * 80)
        report_lines.append("")
        
        for table, columns in sorted(missing.items()):
            report_lines.append(f"Table: {table}")
            for col in sorted(columns):
                report_lines.append(f"  - {col}")
            report_lines.append("")
    
    # Recommendations
    report_lines.append("-" * 80)
    report_lines.append("RECOMMENDATIONS")
    report_lines.append("-" * 80)
    report_lines.append("")
    report_lines.append("1. Review each missing column to determine if it's genuinely needed")
    report_lines.append("2. Create migration scripts for confirmed missing columns")
    report_lines.append("3. Use scripts/safe_add_columns.py to add columns safely")
    report_lines.append("4. Update code to handle missing columns gracefully if not migrating")
    report_lines.append("")
    
    # Write report
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text('\n'.join(report_lines), encoding='utf-8')
    
    # Print to console
    if verbose:
        print('\n'.join(report_lines))
    else:
        # Print summary only
        print(f"Found missing columns in {total_tables} table(s)")
        print(f"Total missing columns: {total_columns}")
        print(f"Report written to: {output_file}")


def main():
    parser = argparse.ArgumentParser(description='Audit database schema for missing columns')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed output')
    parser.add_argument('--table', '-t', help='Check specific table only')
    parser.add_argument('--output', '-o', default='reports/missing_columns_report.txt',
                       help='Output file path')
    args = parser.parse_args()
    
    root_dir = Path.cwd()
    db_path = get_db_path()
    
    if not db_path.exists():
        print(f"Warning: Database not found at {db_path}")
        print("Creating empty database for schema initialization...")
        db_path.parent.mkdir(parents=True, exist_ok=True)
        # Create empty database
        conn = sqlite3.connect(str(db_path))
        conn.close()
    
    print(f"Auditing database: {db_path}")
    print(f"Scanning code in: {root_dir}")
    print()
    
    # Get database schema
    db_schema = get_table_columns(db_path)
    print(f"Found {len(db_schema)} tables in database")
    
    # Check known issues first
    known_issues = check_known_missing_columns(db_schema)
    
    # Scan code for missing columns
    print("Scanning code for column references...")
    missing = find_missing_columns(db_path, root_dir)
    
    # Filter by specific table if requested
    if args.table:
        missing = {k: v for k, v in missing.items() if k == args.table}
        known_issues = {k: v for k, v in known_issues.items() if k == args.table}
    
    # Generate report
    output_path = Path(args.output)
    generate_report(missing, known_issues, output_path, args.verbose)
    
    # Return exit code based on findings
    return 1 if (missing or known_issues) else 0


if __name__ == '__main__':
    sys.exit(main())
