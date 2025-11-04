#!/usr/bin/env python3
"""
Generate comprehensive audit reports for the repository.

This script generates various audit reports including:
- SQL_ACCESS_MAP.md: Map of all SQL queries in the codebase
- buvette_AUDIT.md: Audit of the buvette (snack bar) module
- TODOs.md: List of all TODO comments from automated changes
- COLUMN_REMOVAL_CANDIDATES.md: Columns that might be safe to remove

Usage:
    python scripts/generate_audit_reports.py
    python scripts/generate_audit_reports.py --report buvette  # Generate specific report only
"""

import ast
import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict
import argparse


def scan_sql_queries(root_dir: Path) -> Dict[str, List[Tuple[str, int, str]]]:
    """
    Scan all Python files for SQL queries.
    
    Returns:
        Dictionary mapping file_path -> list of (table_name, line_number, query_snippet)
    """
    sql_map = {}
    
    # Patterns to detect SQL queries
    patterns = [
        re.compile(r'(SELECT|INSERT|UPDATE|DELETE|CREATE|DROP|ALTER)\s+', re.IGNORECASE),
        re.compile(r'execute\s*\(\s*["\']', re.IGNORECASE),
        re.compile(r'read_sql', re.IGNORECASE),
    ]
    
    for py_file in root_dir.rglob('*.py'):
        # Skip test files and venv
        if any(skip in str(py_file) for skip in ['test', 'venv', '.venv', '__pycache__']):
            continue
        
        try:
            content = py_file.read_text(encoding='utf-8', errors='ignore')
            lines = content.split('\n')
            
            queries = []
            for i, line in enumerate(lines, 1):
                # Check if line contains SQL
                if any(pattern.search(line) for pattern in patterns):
                    # Try to extract table name
                    table_match = re.search(r'(?:FROM|INTO|UPDATE|TABLE)\s+(\w+)', line, re.IGNORECASE)
                    table_name = table_match.group(1) if table_match else 'Unknown'
                    
                    # Clean up the query snippet
                    query_snippet = line.strip()[:100]
                    queries.append((table_name, i, query_snippet))
            
            if queries:
                rel_path = str(py_file.relative_to(root_dir))
                sql_map[rel_path] = queries
                
        except Exception as e:
            # Skip files that can't be read
            pass
    
    return sql_map


def generate_sql_access_map(root_dir: Path, output_file: Path):
    """Generate SQL_ACCESS_MAP.md report."""
    sql_map = scan_sql_queries(root_dir)
    
    lines = []
    lines.append("# SQL Access Map")
    lines.append("")
    lines.append("This report maps all SQL database access in the codebase.")
    lines.append("")
    lines.append(f"Generated: {Path.cwd()}")
    lines.append("")
    
    # Summary by table
    table_access = defaultdict(list)
    for file_path, queries in sql_map.items():
        for table, line_num, query in queries:
            table_access[table].append((file_path, line_num, query))
    
    lines.append("## Access by Table")
    lines.append("")
    
    for table in sorted(table_access.keys()):
        lines.append(f"### {table}")
        lines.append("")
        
        accesses = table_access[table]
        lines.append(f"Total accesses: {len(accesses)}")
        lines.append("")
        
        # Group by file
        by_file = defaultdict(list)
        for file_path, line_num, query in accesses:
            by_file[file_path].append((line_num, query))
        
        for file_path in sorted(by_file.keys()):
            lines.append(f"**{file_path}**")
            lines.append("")
            for line_num, query in by_file[file_path]:
                lines.append(f"- Line {line_num}: `{query}`")
            lines.append("")
    
    # Write report
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text('\n'.join(lines), encoding='utf-8')
    print(f"✓ Generated: {output_file}")


def scan_buvette_files(root_dir: Path) -> Dict[str, any]:
    """Scan buvette-related files for audit."""
    buvette_files = []
    
    for py_file in root_dir.rglob('*.py'):
        if 'buvette' in py_file.name.lower():
            buvette_files.append(py_file)
    
    return {
        'files': buvette_files,
        'count': len(buvette_files),
    }


def generate_buvette_audit(root_dir: Path, output_file: Path):
    """Generate buvette_AUDIT.md report."""
    data = scan_buvette_files(root_dir)
    
    lines = []
    lines.append("# Buvette Module Audit")
    lines.append("")
    lines.append("Comprehensive audit of the buvette (snack bar) module.")
    lines.append("")
    lines.append(f"Generated: {Path.cwd()}")
    lines.append("")
    
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Total buvette-related files: {data['count']}")
    lines.append("")
    
    lines.append("## Files")
    lines.append("")
    for file in sorted(data['files']):
        rel_path = str(file.relative_to(root_dir))
        size = file.stat().st_size
        lines.append(f"- `{rel_path}` ({size} bytes)")
    lines.append("")
    
    lines.append("## Known Issues")
    lines.append("")
    lines.append("### Missing Columns")
    lines.append("- `buvette_inventaire_lignes.commentaire` - Added via migration 0001")
    lines.append("")
    
    lines.append("## Recommendations")
    lines.append("")
    lines.append("1. Review all buvette database queries for proper error handling")
    lines.append("2. Ensure row_to_dict() is used for all database row access")
    lines.append("3. Add comprehensive tests for buvette inventory operations")
    lines.append("")
    
    # Write report
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text('\n'.join(lines), encoding='utf-8')
    print(f"✓ Generated: {output_file}")


def scan_todos(root_dir: Path) -> List[Tuple[str, int, str]]:
    """Scan for TODO comments in the codebase."""
    todos = []
    
    for py_file in root_dir.rglob('*.py'):
        # Skip test files and venv
        if any(skip in str(py_file) for skip in ['test', 'venv', '.venv', '__pycache__']):
            continue
        
        try:
            content = py_file.read_text(encoding='utf-8', errors='ignore')
            lines = content.split('\n')
            
            for i, line in enumerate(lines, 1):
                if 'TODO' in line or 'FIXME' in line:
                    rel_path = str(py_file.relative_to(root_dir))
                    todos.append((rel_path, i, line.strip()))
                    
        except Exception as e:
            pass
    
    return todos


def generate_todos_report(root_dir: Path, output_file: Path):
    """Generate TODOs.md report."""
    todos = scan_todos(root_dir)
    
    lines = []
    lines.append("# TODO Items Report")
    lines.append("")
    lines.append("This report lists all TODO and FIXME comments in the codebase,")
    lines.append("including those added by automated changes.")
    lines.append("")
    lines.append(f"Generated: {Path.cwd()}")
    lines.append("")
    
    lines.append(f"## Summary")
    lines.append("")
    lines.append(f"Total TODO/FIXME items: {len(todos)}")
    lines.append("")
    
    # Group by file
    by_file = defaultdict(list)
    for file_path, line_num, comment in todos:
        by_file[file_path].append((line_num, comment))
    
    lines.append("## Items by File")
    lines.append("")
    
    for file_path in sorted(by_file.keys()):
        lines.append(f"### {file_path}")
        lines.append("")
        for line_num, comment in by_file[file_path]:
            lines.append(f"- Line {line_num}: {comment}")
        lines.append("")
    
    # Write report
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text('\n'.join(lines), encoding='utf-8')
    print(f"✓ Generated: {output_file}")


def generate_column_removal_candidates(root_dir: Path, output_file: Path):
    """Generate COLUMN_REMOVAL_CANDIDATES.md report."""
    lines = []
    lines.append("# Column Removal Candidates")
    lines.append("")
    lines.append("This report lists database columns that *might* be safe to remove.")
    lines.append("⚠️  **CAUTION**: This is for reference only. Never remove columns without thorough testing.")
    lines.append("")
    lines.append(f"Generated: {Path.cwd()}")
    lines.append("")
    
    lines.append("## Methodology")
    lines.append("")
    lines.append("Columns are considered candidates for removal if:")
    lines.append("- They are rarely or never queried in the codebase")
    lines.append("- They contain mostly NULL values")
    lines.append("- They were added for features that are no longer used")
    lines.append("")
    
    lines.append("## Candidates")
    lines.append("")
    lines.append("*No automatic detection implemented yet.*")
    lines.append("")
    lines.append("Manual review required. Check:")
    lines.append("- Database column usage statistics")
    lines.append("- Feature usage analytics")
    lines.append("- Historical commit messages")
    lines.append("")
    
    lines.append("## Recommendation")
    lines.append("")
    lines.append("Instead of removing columns:")
    lines.append("1. Mark them as deprecated in documentation")
    lines.append("2. Add a migration to remove them in a future version")
    lines.append("3. Keep them for backward compatibility if unsure")
    lines.append("")
    
    # Write report
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text('\n'.join(lines), encoding='utf-8')
    print(f"✓ Generated: {output_file}")


def main():
    parser = argparse.ArgumentParser(description='Generate audit reports')
    parser.add_argument('--report', choices=['sql', 'buvette', 'todos', 'removal', 'all'],
                       default='all', help='Which report(s) to generate')
    args = parser.parse_args()
    
    root_dir = Path.cwd()
    reports_dir = root_dir / 'reports'
    reports_dir.mkdir(exist_ok=True)
    
    print("=" * 70)
    print("Generating Audit Reports")
    print("=" * 70)
    print()
    
    # Generate requested reports
    if args.report in ['sql', 'all']:
        generate_sql_access_map(root_dir, reports_dir / 'SQL_ACCESS_MAP.md')
    
    if args.report in ['buvette', 'all']:
        generate_buvette_audit(root_dir, reports_dir / 'buvette_AUDIT.md')
    
    if args.report in ['todos', 'all']:
        generate_todos_report(root_dir, reports_dir / 'TODOs.md')
    
    if args.report in ['removal', 'all']:
        generate_column_removal_candidates(root_dir, reports_dir / 'COLUMN_REMOVAL_CANDIDATES.md')
    
    print()
    print("✓ All reports generated successfully!")
    print(f"  Output directory: {reports_dir}")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
