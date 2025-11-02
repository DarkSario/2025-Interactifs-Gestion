#!/usr/bin/env python3
"""
Database Usage Audit Script

Scans the codebase for:
- sqlite3 usage patterns
- fetch/execute patterns
- row.get usages
- positional indexing (row[0], row[1], etc.)
- Generate reports in reports/SQL_ACCESS_MAP.md and reports/TODOs.md

This script helps identify areas where sqlite3.Row objects are used with .get()
method (which causes AttributeError) and need to be converted to dicts.
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Set
from datetime import datetime


class DBUsageAuditor:
    """Auditor for database access patterns in Python codebase."""
    
    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)
        self.results = {
            'sqlite3_imports': [],
            'get_connection_calls': [],
            'fetch_patterns': [],
            'row_get_usage': [],
            'positional_indexing': [],
            'execute_patterns': [],
            'connection_patterns': [],
        }
        
    def scan_file(self, filepath: Path) -> Dict:
        """Scan a single Python file for DB usage patterns."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
        except (UnicodeDecodeError, PermissionError) as e:
            return {}
        
        rel_path = filepath.relative_to(self.root_dir)
        file_results = {}
        
        # Pattern: import sqlite3
        if re.search(r'import\s+sqlite3', content):
            self.results['sqlite3_imports'].append({
                'file': str(rel_path),
                'line': self._find_line_number(lines, r'import\s+sqlite3')
            })
        
        # Pattern: get_connection()
        for match in re.finditer(r'(\w+\.)?get_connection\(\)', content):
            line_num = self._get_line_number(content, match.start())
            self.results['get_connection_calls'].append({
                'file': str(rel_path),
                'line': line_num,
                'code': lines[line_num - 1].strip() if line_num <= len(lines) else ''
            })
        
        # Pattern: fetchone(), fetchall(), fetchmany()
        for pattern in [r'\.fetchone\(\)', r'\.fetchall\(\)', r'\.fetchmany\(']:
            for match in re.finditer(pattern, content):
                line_num = self._get_line_number(content, match.start())
                self.results['fetch_patterns'].append({
                    'file': str(rel_path),
                    'line': line_num,
                    'pattern': match.group(),
                    'code': lines[line_num - 1].strip() if line_num <= len(lines) else ''
                })
        
        # Pattern: row.get( or row.get('
        for match in re.finditer(r'(\w+)\.get\(["\']', content):
            line_num = self._get_line_number(content, match.start())
            var_name = match.group(1)
            # Check if this might be a row variable
            if var_name in ['row', 'r', 'res', 'result', 'item', 'data'] or 'row' in var_name.lower():
                self.results['row_get_usage'].append({
                    'file': str(rel_path),
                    'line': line_num,
                    'variable': var_name,
                    'code': lines[line_num - 1].strip() if line_num <= len(lines) else ''
                })
        
        # Pattern: row[0], row[1], etc. (positional indexing)
        for match in re.finditer(r'(\w+)\[(\d+)\]', content):
            line_num = self._get_line_number(content, match.start())
            var_name = match.group(1)
            index = match.group(2)
            # Check if this might be a row variable
            if var_name in ['row', 'r', 'res', 'result', 'item', 'data'] or 'row' in var_name.lower():
                self.results['positional_indexing'].append({
                    'file': str(rel_path),
                    'line': line_num,
                    'variable': var_name,
                    'index': index,
                    'code': lines[line_num - 1].strip() if line_num <= len(lines) else ''
                })
        
        # Pattern: .execute(
        for match in re.finditer(r'\.execute\(', content):
            line_num = self._get_line_number(content, match.start())
            # Get the full statement (might span multiple lines)
            code_snippet = self._get_code_snippet(lines, line_num - 1, 3)
            self.results['execute_patterns'].append({
                'file': str(rel_path),
                'line': line_num,
                'code': code_snippet
            })
        
        # Pattern: sqlite3.connect(
        for match in re.finditer(r'sqlite3\.connect\(', content):
            line_num = self._get_line_number(content, match.start())
            self.results['connection_patterns'].append({
                'file': str(rel_path),
                'line': line_num,
                'code': lines[line_num - 1].strip() if line_num <= len(lines) else ''
            })
        
        return file_results
    
    def _find_line_number(self, lines: List[str], pattern: str) -> int:
        """Find the first line number matching a pattern."""
        for i, line in enumerate(lines, 1):
            if re.search(pattern, line):
                return i
        return 0
    
    def _get_line_number(self, content: str, char_pos: int) -> int:
        """Get line number from character position."""
        return content[:char_pos].count('\n') + 1
    
    def _get_code_snippet(self, lines: List[str], start_line: int, num_lines: int = 1) -> str:
        """Get a snippet of code from multiple lines."""
        end_line = min(start_line + num_lines, len(lines))
        return ' '.join(lines[start_line:end_line]).strip()
    
    def scan_directory(self, directory: Path = None):
        """Recursively scan directory for Python files."""
        if directory is None:
            directory = self.root_dir
        
        # Directories to skip
        skip_dirs = {'.git', '__pycache__', 'venv', 'env', '.pytest_cache', 'node_modules', 'dist', 'build'}
        
        for item in directory.iterdir():
            if item.is_dir():
                if item.name not in skip_dirs:
                    self.scan_directory(item)
            elif item.suffix == '.py':
                self.scan_file(item)
    
    def generate_sql_access_map(self) -> str:
        """Generate SQL_ACCESS_MAP.md report."""
        report = []
        report.append("# SQL Access Map\n")
        report.append(f"Generated: {datetime.now().isoformat()}\n")
        report.append("This report maps all database access patterns in the codebase.\n")
        
        report.append("\n## Summary\n")
        report.append(f"- sqlite3 imports: {len(self.results['sqlite3_imports'])}\n")
        report.append(f"- get_connection() calls: {len(self.results['get_connection_calls'])}\n")
        report.append(f"- fetch patterns: {len(self.results['fetch_patterns'])}\n")
        report.append(f"- row.get() usage: {len(self.results['row_get_usage'])}\n")
        report.append(f"- Positional indexing: {len(self.results['positional_indexing'])}\n")
        report.append(f"- execute() calls: {len(self.results['execute_patterns'])}\n")
        report.append(f"- sqlite3.connect() calls: {len(self.results['connection_patterns'])}\n")
        
        # sqlite3 imports
        if self.results['sqlite3_imports']:
            report.append("\n## SQLite3 Imports\n")
            for item in self.results['sqlite3_imports']:
                report.append(f"- `{item['file']}:{item['line']}`\n")
        
        # get_connection calls
        if self.results['get_connection_calls']:
            report.append("\n## get_connection() Calls\n")
            files_with_calls = {}
            for item in self.results['get_connection_calls']:
                file = item['file']
                if file not in files_with_calls:
                    files_with_calls[file] = []
                files_with_calls[file].append(item)
            
            for file, calls in sorted(files_with_calls.items()):
                report.append(f"\n### {file}\n")
                for call in calls:
                    report.append(f"- Line {call['line']}: `{call['code']}`\n")
        
        # Fetch patterns
        if self.results['fetch_patterns']:
            report.append("\n## Fetch Patterns\n")
            files_with_fetches = {}
            for item in self.results['fetch_patterns']:
                file = item['file']
                if file not in files_with_fetches:
                    files_with_fetches[file] = []
                files_with_fetches[file].append(item)
            
            for file, fetches in sorted(files_with_fetches.items()):
                report.append(f"\n### {file}\n")
                for fetch in fetches:
                    report.append(f"- Line {fetch['line']} `{fetch['pattern']}`: `{fetch['code']}`\n")
        
        # Row.get usage (CRITICAL - these will crash)
        if self.results['row_get_usage']:
            report.append("\n## ⚠️ CRITICAL: row.get() Usage (Will Crash!)\n")
            report.append("These locations use .get() on sqlite3.Row objects, which will cause AttributeError.\n")
            report.append("These MUST be fixed by converting rows to dicts first.\n")
            files_with_get = {}
            for item in self.results['row_get_usage']:
                file = item['file']
                if file not in files_with_get:
                    files_with_get[file] = []
                files_with_get[file].append(item)
            
            for file, gets in sorted(files_with_get.items()):
                report.append(f"\n### {file}\n")
                for get in gets:
                    report.append(f"- Line {get['line']} (var: `{get['variable']}`): `{get['code']}`\n")
        
        # Positional indexing
        if self.results['positional_indexing']:
            report.append("\n## Positional Indexing (row[0], row[1], ...)\n")
            report.append("These use positional access and should continue to work.\n")
            files_with_pos = {}
            for item in self.results['positional_indexing']:
                file = item['file']
                if file not in files_with_pos:
                    files_with_pos[file] = []
                files_with_pos[file].append(item)
            
            for file, positions in sorted(files_with_pos.items()):
                report.append(f"\n### {file}\n")
                unique_lines = {}
                for pos in positions:
                    line_key = f"{pos['line']}"
                    if line_key not in unique_lines:
                        unique_lines[line_key] = pos
                
                for pos in unique_lines.values():
                    report.append(f"- Line {pos['line']}: `{pos['code']}`\n")
        
        return ''.join(report)
    
    def generate_todos(self) -> str:
        """Generate TODOs.md report with action items."""
        report = []
        report.append("# Database Access TODOs\n")
        report.append(f"Generated: {datetime.now().isoformat()}\n")
        report.append("\nThis report lists action items for fixing database access issues.\n")
        
        # Critical fixes needed
        if self.results['row_get_usage']:
            report.append("\n## 🔴 CRITICAL: Fix row.get() Usage\n")
            report.append("Priority: **HIGH** - These will cause AttributeError crashes\n")
            report.append("\nAction: Convert sqlite3.Row to dict before using .get()\n")
            report.append("Solution: Use `_row_to_dict(row)` or `_rows_to_dicts(rows)` from modules/db_row_utils.py\n")
            
            for item in self.results['row_get_usage']:
                report.append(f"\n- [ ] {item['file']}:{item['line']}\n")
                report.append(f"  ```python\n  {item['code']}\n  ```\n")
        
        # Direct sqlite3.connect usage
        if self.results['connection_patterns']:
            report.append("\n## 🟡 RECOMMENDED: Standardize Connection Handling\n")
            report.append("Priority: **MEDIUM** - Should use centralized connection management\n")
            report.append("\nAction: Use db.get_connection() or modules.db_api.get_connection() instead of direct sqlite3.connect()\n")
            report.append("Benefit: Automatic WAL mode, busy timeout, and consistent error handling\n")
            
            for item in self.results['connection_patterns']:
                report.append(f"\n- [ ] {item['file']}:{item['line']}\n")
                report.append(f"  ```python\n  {item['code']}\n  ```\n")
        
        # Fetch patterns without conversion
        fetch_files = set(item['file'] for item in self.results['fetch_patterns'])
        get_files = set(item['file'] for item in self.results['row_get_usage'])
        
        # Files with fetch but no documented .get() issues might still be at risk
        at_risk_files = fetch_files - get_files
        if at_risk_files:
            report.append("\n## 🟢 LOW PRIORITY: Review Fetch Patterns\n")
            report.append("These files use fetch patterns but don't show .get() usage in this scan.\n")
            report.append("Review to ensure they don't need dict conversion.\n")
            for file in sorted(at_risk_files):
                report.append(f"- [ ] {file}\n")
        
        return ''.join(report)


def main():
    """Main entry point for the audit script."""
    # Find root directory
    script_dir = Path(__file__).parent
    root_dir = script_dir.parent
    
    print("=" * 70)
    print("Database Usage Audit Tool")
    print("=" * 70)
    print(f"\nScanning directory: {root_dir}")
    print("This may take a moment...\n")
    
    # Create auditor and scan
    auditor = DBUsageAuditor(root_dir)
    auditor.scan_directory()
    
    # Create reports directory if it doesn't exist
    reports_dir = root_dir / 'reports'
    reports_dir.mkdir(exist_ok=True)
    
    # Generate and write reports
    print("Generating SQL_ACCESS_MAP.md...")
    sql_map = auditor.generate_sql_access_map()
    sql_map_path = reports_dir / 'SQL_ACCESS_MAP.md'
    with open(sql_map_path, 'w', encoding='utf-8') as f:
        f.write(sql_map)
    print(f"✓ Written to {sql_map_path}")
    
    print("\nGenerating TODOs.md...")
    todos = auditor.generate_todos()
    todos_path = reports_dir / 'TODOs.md'
    with open(todos_path, 'w', encoding='utf-8') as f:
        f.write(todos)
    print(f"✓ Written to {todos_path}")
    
    print("\n" + "=" * 70)
    print("Audit Complete!")
    print("=" * 70)
    print(f"\nSummary:")
    print(f"  - row.get() issues found: {len(auditor.results['row_get_usage'])}")
    print(f"  - Direct sqlite3.connect() calls: {len(auditor.results['connection_patterns'])}")
    print(f"  - Total fetch patterns: {len(auditor.results['fetch_patterns'])}")
    print(f"\nReview the reports in {reports_dir}/ for details.")
    
    # Return exit code based on critical issues
    if auditor.results['row_get_usage']:
        print("\n⚠️  CRITICAL issues found! See TODOs.md for action items.")
        return 1
    else:
        print("\n✓ No critical issues found.")
        return 0


if __name__ == '__main__':
    sys.exit(main())
