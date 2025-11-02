#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database Diagnostics Script

This script performs health checks on the SQLite database to diagnose
issues related to:
- Database locks
- WAL mode configuration
- Connection settings
- Table integrity
- Common sqlite3.Row conversion issues

Usage:
    python scripts/db_diagnostics.py [--db-path PATH] [--output REPORT_FILE]
    
Example:
    python scripts/db_diagnostics.py
    python scripts/db_diagnostics.py --db-path association.db --output reports/db_health.txt
"""

import sqlite3
import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Any

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from db.db import get_db_file, get_connection
from utils.app_logger import get_logger

logger = get_logger("db_diagnostics")


class DBDiagnostics:
    """Database diagnostics and health check utility."""
    
    def __init__(self, db_path: str = None):
        """
        Initialize diagnostics.
        
        Args:
            db_path: Path to database file (optional, uses default if not provided)
        """
        self.db_path = db_path or get_db_file()
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'db_path': self.db_path,
            'checks': {},
            'errors': [],
            'warnings': []
        }
    
    def check_file_exists(self) -> bool:
        """Check if database file exists."""
        exists = os.path.exists(self.db_path)
        self.results['checks']['file_exists'] = exists
        if not exists:
            self.results['errors'].append(f"Database file not found: {self.db_path}")
        return exists
    
    def check_file_permissions(self) -> bool:
        """Check if database file is readable and writable."""
        try:
            readable = os.access(self.db_path, os.R_OK)
            writable = os.access(self.db_path, os.W_OK)
            
            self.results['checks']['file_readable'] = readable
            self.results['checks']['file_writable'] = writable
            
            if not readable:
                self.results['errors'].append("Database file is not readable")
            if not writable:
                self.results['warnings'].append("Database file is not writable")
            
            return readable and writable
        except Exception as e:
            self.results['errors'].append(f"Error checking file permissions: {e}")
            return False
    
    def check_wal_mode(self) -> Tuple[bool, str]:
        """Check if WAL mode is enabled."""
        try:
            conn = sqlite3.connect(self.db_path, timeout=5)
            cursor = conn.cursor()
            cursor.execute("PRAGMA journal_mode;")
            mode = cursor.fetchone()[0]
            conn.close()
            
            is_wal = mode.upper() == 'WAL'
            self.results['checks']['wal_mode'] = mode
            
            if not is_wal:
                self.results['warnings'].append(
                    f"WAL mode not enabled (current: {mode}). "
                    "Consider running scripts/enable_wal.py"
                )
            
            return is_wal, mode
        except Exception as e:
            self.results['errors'].append(f"Error checking WAL mode: {e}")
            return False, "unknown"
    
    def check_busy_timeout(self) -> int:
        """Check busy timeout configuration."""
        try:
            conn = sqlite3.connect(self.db_path, timeout=5)
            cursor = conn.cursor()
            cursor.execute("PRAGMA busy_timeout;")
            timeout = cursor.fetchone()[0]
            conn.close()
            
            self.results['checks']['busy_timeout'] = timeout
            
            if timeout < 5000:
                self.results['warnings'].append(
                    f"Busy timeout is low ({timeout}ms). "
                    "Recommended: 5000ms or higher to reduce lock errors"
                )
            
            return timeout
        except Exception as e:
            self.results['errors'].append(f"Error checking busy timeout: {e}")
            return 0
    
    def check_database_integrity(self) -> bool:
        """Run SQLite integrity check."""
        try:
            conn = sqlite3.connect(self.db_path, timeout=5)
            cursor = conn.cursor()
            cursor.execute("PRAGMA integrity_check;")
            result = cursor.fetchone()[0]
            conn.close()
            
            is_ok = result.lower() == 'ok'
            self.results['checks']['integrity_check'] = result
            
            if not is_ok:
                self.results['errors'].append(f"Database integrity check failed: {result}")
            
            return is_ok
        except Exception as e:
            self.results['errors'].append(f"Error running integrity check: {e}")
            return False
    
    def check_connection(self) -> bool:
        """Test basic database connection."""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT 1;")
            cursor.fetchone()
            conn.close()
            
            self.results['checks']['connection_test'] = "OK"
            return True
        except Exception as e:
            self.results['errors'].append(f"Connection test failed: {e}")
            self.results['checks']['connection_test'] = f"FAILED: {e}"
            return False
    
    def check_row_factory(self) -> bool:
        """Check if row_factory is properly configured."""
        try:
            conn = get_connection()
            has_row_factory = conn.row_factory is not None
            factory_type = type(conn.row_factory).__name__ if has_row_factory else "None"
            conn.close()
            
            self.results['checks']['row_factory'] = factory_type
            
            if not has_row_factory:
                self.results['warnings'].append(
                    "No row_factory configured. Consider using sqlite3.Row for named access"
                )
            
            return has_row_factory
        except Exception as e:
            self.results['errors'].append(f"Error checking row_factory: {e}")
            return False
    
    def list_tables(self) -> List[str]:
        """List all tables in the database."""
        try:
            conn = sqlite3.connect(self.db_path, timeout=5)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' 
                ORDER BY name;
            """)
            tables = [row[0] for row in cursor.fetchall()]
            conn.close()
            
            self.results['checks']['table_count'] = len(tables)
            self.results['checks']['tables'] = tables
            
            return tables
        except Exception as e:
            self.results['errors'].append(f"Error listing tables: {e}")
            return []
    
    def check_table_sizes(self) -> Dict[str, int]:
        """Get row counts for all tables."""
        tables = self.list_tables()
        sizes = {}
        
        try:
            conn = sqlite3.connect(self.db_path, timeout=5)
            cursor = conn.cursor()
            
            for table in tables:
                try:
                    # Use identifier quoting to prevent SQL injection
                    # sqlite_master returns trusted table names, but use quoting for safety
                    quoted_table = f'"{table}"'
                    cursor.execute(f"SELECT COUNT(*) FROM {quoted_table};")
                    count = cursor.fetchone()[0]
                    sizes[table] = count
                except Exception as e:
                    sizes[table] = f"Error: {e}"
            
            conn.close()
            self.results['checks']['table_sizes'] = sizes
            
            return sizes
        except Exception as e:
            self.results['errors'].append(f"Error checking table sizes: {e}")
            return {}
    
    def run_all_checks(self) -> Dict[str, Any]:
        """Run all diagnostic checks."""
        print("Running database diagnostics...\n")
        
        # Basic file checks
        print("1. Checking database file...")
        if not self.check_file_exists():
            return self.results
        self.check_file_permissions()
        
        # Configuration checks
        print("2. Checking database configuration...")
        self.check_wal_mode()
        self.check_busy_timeout()
        self.check_row_factory()
        
        # Connection tests
        print("3. Testing database connection...")
        self.check_connection()
        
        # Integrity checks
        print("4. Running integrity check...")
        self.check_database_integrity()
        
        # Table information
        print("5. Gathering table information...")
        self.list_tables()
        self.check_table_sizes()
        
        print("\nDiagnostics complete!\n")
        return self.results
    
    def generate_report(self, output_file: str = None) -> str:
        """
        Generate a human-readable report.
        
        Args:
            output_file: Optional file path to write report to
            
        Returns:
            str: Report text
        """
        lines = []
        lines.append("=" * 80)
        lines.append("DATABASE DIAGNOSTICS REPORT")
        lines.append("=" * 80)
        lines.append(f"Timestamp: {self.results['timestamp']}")
        lines.append(f"Database: {self.results['db_path']}")
        lines.append("")
        
        # Summary
        error_count = len(self.results['errors'])
        warning_count = len(self.results['warnings'])
        
        lines.append("SUMMARY")
        lines.append("-" * 80)
        if error_count == 0 and warning_count == 0:
            lines.append("✓ All checks passed!")
        else:
            if error_count > 0:
                lines.append(f"✗ {error_count} error(s) found")
            if warning_count > 0:
                lines.append(f"⚠ {warning_count} warning(s) found")
        lines.append("")
        
        # Errors
        if self.results['errors']:
            lines.append("ERRORS")
            lines.append("-" * 80)
            for error in self.results['errors']:
                lines.append(f"✗ {error}")
            lines.append("")
        
        # Warnings
        if self.results['warnings']:
            lines.append("WARNINGS")
            lines.append("-" * 80)
            for warning in self.results['warnings']:
                lines.append(f"⚠ {warning}")
            lines.append("")
        
        # Detailed checks
        lines.append("DETAILED CHECKS")
        lines.append("-" * 80)
        checks = self.results['checks']
        
        for key, value in checks.items():
            if key == 'tables':
                lines.append(f"Tables: {', '.join(value) if value else 'None'}")
            elif key == 'table_sizes':
                lines.append("Table Sizes:")
                for table, size in value.items():
                    lines.append(f"  - {table}: {size} rows")
            else:
                lines.append(f"{key}: {value}")
        
        lines.append("")
        lines.append("=" * 80)
        
        report = '\n'.join(lines)
        
        # Write to file if requested
        if output_file:
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(report)
                print(f"\nReport written to: {output_file}")
            except Exception as e:
                print(f"\nError writing report: {e}")
        
        return report


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Run database diagnostics and health checks"
    )
    parser.add_argument(
        '--db-path',
        help='Path to database file (optional, uses default if not provided)'
    )
    parser.add_argument(
        '--output',
        help='Output file for report (optional, prints to stdout if not provided)'
    )
    
    args = parser.parse_args()
    
    # Run diagnostics
    diagnostics = DBDiagnostics(db_path=args.db_path)
    diagnostics.run_all_checks()
    
    # Generate and display report
    report = diagnostics.generate_report(output_file=args.output)
    print(report)
    
    # Exit with error code if errors found
    if diagnostics.results['errors']:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
