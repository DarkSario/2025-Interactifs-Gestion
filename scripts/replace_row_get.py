#!/usr/bin/env python3
"""
AST-based replacer: detect and fix unsafe row.get() usage patterns.

This script identifies code that uses .get() on variables that might be sqlite3.Row objects,
which don't have a .get() method. It suggests or applies fixes by adding row_to_dict conversions.

Usage:
    python scripts/replace_row_get.py              # Dry-run, show potential issues
    python scripts/replace_row_get.py --apply      # Apply fixes automatically
    python scripts/replace_row_get.py --file path  # Check specific file

The script detects patterns like:
    - row.get('column')
    - result.get('field', default)
    - item.get('key')

And suggests wrapping with row_to_dict() or converting the variable assignment.
"""

import ast
import sys
from pathlib import Path
from typing import List, Set, Tuple, Optional
import argparse


# Directories to skip during scanning
SKIP_DIRS = {'.git', '__pycache__', 'venv', 'env', '.pytest_cache', 'node_modules', 'dist', 'build', 'reports'}

# Variable names that commonly hold database rows
ROW_VAR_NAMES = {'row', 'r', 'res', 'result', 'item', 'data', 'record', 'member', 'article', 'event'}


class RowGetDetector(ast.NodeVisitor):
    """
    AST visitor that detects potentially unsafe .get() calls on row-like variables.
    """
    
    def __init__(self, source_lines: List[str]):
        self.source_lines = source_lines
        self.issues: List[Tuple[int, str, str]] = []  # (line_number, variable_name, code_snippet)
        self.suspicious_vars: Set[str] = set()
        
    def visit_Call(self, node: ast.Call):
        """Visit function call nodes to detect .get() calls."""
        # Check if this is a method call (attribute access)
        if isinstance(node.func, ast.Attribute):
            # Check if the method is 'get'
            if node.func.attr == 'get':
                # Get the variable name being called
                var_name = self._get_var_name(node.func.value)
                
                # Check if this variable name looks like it could be a database row
                if var_name and self._is_suspicious_var(var_name):
                    line_num = node.lineno
                    code_snippet = self._get_code_snippet(line_num)
                    self.issues.append((line_num, var_name, code_snippet))
        
        self.generic_visit(node)
    
    def _get_var_name(self, node: ast.AST) -> Optional[str]:
        """Extract variable name from an AST node."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Subscript):
            # Handle cases like rows[i].get()
            return self._get_var_name(node.value)
        return None
    
    def _is_suspicious_var(self, var_name: str) -> bool:
        """
        Check if a variable name suggests it might be a database row.
        
        Returns True if:
        - Variable name is in common row variable names
        - Variable name contains 'row' substring
        """
        var_lower = var_name.lower()
        
        # Check exact matches
        if var_lower in ROW_VAR_NAMES:
            return True
        
        # Check if 'row' appears in the name
        if 'row' in var_lower:
            return True
        
        # Check for common patterns
        if var_lower.endswith('_row') or var_lower.startswith('row_'):
            return True
        
        return False
    
    def _get_code_snippet(self, line_num: int) -> str:
        """Get the source code for a given line number."""
        if 0 < line_num <= len(self.source_lines):
            return self.source_lines[line_num - 1].strip()
        return ""


class RowGetTransformer(ast.NodeTransformer):
    """
    AST transformer that wraps row variables with row_to_dict() conversion.
    
    This is a simplified transformer that can be extended for automatic fixes.
    Currently, it's used for analysis rather than automatic transformation,
    as automatic fixes require careful context analysis.
    """
    
    def __init__(self):
        self.changes_made = False
        self.import_needed = False


def scan_file(file_path: Path, apply_fixes: bool = False) -> Tuple[List[Tuple[int, str, str]], bool]:
    """
    Scan a Python file for unsafe row.get() usage.
    
    Args:
        file_path: Path to the Python file
        apply_fixes: If True, attempt to apply automatic fixes (not yet implemented)
        
    Returns:
        Tuple of (list of issues, whether changes were made)
    """
    try:
        source = file_path.read_text(encoding='utf-8')
        source_lines = source.split('\n')
    except (UnicodeDecodeError, PermissionError) as e:
        return [], False
    
    try:
        tree = ast.parse(source, filename=str(file_path))
    except SyntaxError:
        # Skip files with syntax errors
        return [], False
    
    # Detect issues
    detector = RowGetDetector(source_lines)
    detector.visit(tree)
    
    # TODO: Implement automatic fixes using RowGetTransformer
    # For now, we only detect issues
    
    return detector.issues, False


def should_skip_path(path: Path) -> bool:
    """Check if a path should be skipped during scanning."""
    return any(skip_dir in path.parts for skip_dir in SKIP_DIRS)


def scan_directory(root_dir: Path, apply_fixes: bool = False) -> dict:
    """
    Recursively scan directory for Python files with row.get() issues.
    
    Args:
        root_dir: Root directory to scan
        apply_fixes: If True, attempt to apply automatic fixes
        
    Returns:
        Dictionary mapping file paths to lists of issues
    """
    results = {}
    
    for py_file in root_dir.rglob('*.py'):
        if should_skip_path(py_file):
            continue
        
        issues, changed = scan_file(py_file, apply_fixes)
        if issues:
            rel_path = py_file.relative_to(root_dir)
            results[str(rel_path)] = issues
    
    return results


def print_report(results: dict) -> None:
    """Print a formatted report of detected issues."""
    if not results:
        print("✓ No unsafe row.get() patterns detected!")
        return
    
    total_issues = sum(len(issues) for issues in results.values())
    
    print("=" * 80)
    print(f"Row.get() Usage Detection Report")
    print("=" * 80)
    print(f"\nFound {total_issues} potential issues in {len(results)} files\n")
    print("These locations use .get() on variables that might be sqlite3.Row objects.")
    print("sqlite3.Row does not have a .get() method and will raise AttributeError.\n")
    print("Recommended fix: Convert to dict using row_to_dict() from src.db.row_utils\n")
    
    for file_path, issues in sorted(results.items()):
        print(f"\n📄 {file_path}")
        print("-" * 80)
        for line_num, var_name, code_snippet in issues:
            print(f"  Line {line_num}: {var_name}.get(...)")
            print(f"    {code_snippet}")
    
    print("\n" + "=" * 80)
    print("Next steps:")
    print("  1. Review each location to determine if the variable is a sqlite3.Row")
    print("  2. If it is, wrap with row_to_dict(): var = row_to_dict(var)")
    print("  3. Or update the source to return dicts from repository methods")
    print("  4. Add: from src.db.row_utils import row_to_dict")
    print("=" * 80)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Detect and fix unsafe row.get() usage patterns',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/replace_row_get.py                    # Scan entire repository
  python scripts/replace_row_get.py --file modules/buvette_db.py  # Check specific file
  python scripts/replace_row_get.py --apply            # Apply fixes (not yet implemented)
        """
    )
    
    parser.add_argument('--apply', action='store_true',
                        help='Apply fixes automatically (not yet implemented)')
    parser.add_argument('--file', type=Path,
                        help='Check a specific file instead of scanning all')
    
    args = parser.parse_args()
    
    # Find root directory
    script_dir = Path(__file__).parent
    root_dir = script_dir.parent
    
    print(f"Scanning from: {root_dir}\n")
    
    if args.file:
        # Scan single file
        if not args.file.exists():
            print(f"Error: File not found: {args.file}")
            return 1
        
        issues, changed = scan_file(args.file, args.apply)
        if issues:
            results = {str(args.file): issues}
            print_report(results)
        else:
            print(f"✓ No issues found in {args.file}")
        
        return 1 if issues else 0
    else:
        # Scan entire directory
        results = scan_directory(root_dir, args.apply)
        print_report(results)
        
        return 1 if results else 0


if __name__ == '__main__':
    sys.exit(main())
