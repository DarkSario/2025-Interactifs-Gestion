#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto-fix script for sqlite3.Row to dict conversions in buvette/inventory modules.

This script heuristically scans modules/ and ui/ directories for patterns where:
- rows = cursor.fetchall() or row = cursor.fetchone() are used
- followed by .get() calls on those rows

For each matching file it:
1. Creates a backup copy <file>.bak
2. Injects imports: from modules.db_row_utils import _row_to_dict, _rows_to_dicts
3. Injects conversions after fetchone/fetchall calls
4. Writes a patch diff file <file>.fix.diff for reviewer
5. Applies the changes to the working file

Note: This script is designed to be safe and non-destructive. It always creates
backups before modifying files and generates diff files for human review.
"""

import difflib
import os
import re
import sys
import shutil
from pathlib import Path
from datetime import datetime


def find_python_files(base_dir, subdirs=None):
    """Find all Python files in specified subdirectories."""
    if subdirs is None:
        subdirs = ['modules', 'ui']
    
    python_files = []
    for subdir in subdirs:
        search_path = os.path.join(base_dir, subdir)
        if os.path.exists(search_path):
            for root, _, files in os.walk(search_path):
                for file in files:
                    if file.endswith('.py'):
                        python_files.append(os.path.join(root, file))
    
    return python_files


def has_fetchall_or_fetchone(content):
    """Check if file contains fetchall() or fetchone() calls."""
    return bool(re.search(r'\.(fetchall|fetchone)\(\)', content))


def has_get_usage(content):
    """Check if file uses .get() method on potential row objects."""
    # Look for patterns like: row.get(, row_var.get(, rows[i].get(, etc.
    return bool(re.search(r'(row|ligne|line|result)[\w]*\.get\(', content))


def needs_db_row_utils_import(content):
    """Check if file needs the db_row_utils import."""
    has_import = re.search(r'from modules\.db_row_utils import', content)
    return not has_import


def inject_import(content):
    """Inject the db_row_utils import after other module imports."""
    # Find the last import statement
    lines = content.split('\n')
    last_import_idx = -1
    
    for idx, line in enumerate(lines):
        if line.strip().startswith(('import ', 'from ')):
            last_import_idx = idx
    
    if last_import_idx >= 0:
        # Insert after the last import
        import_line = 'from modules.db_row_utils import _row_to_dict, _rows_to_dicts'
        lines.insert(last_import_idx + 1, import_line)
        return '\n'.join(lines)
    else:
        # No imports found, insert at top after docstring
        # Find end of docstring if present
        insert_idx = 0
        if content.startswith('"""') or content.startswith("'''"):
            delimiter = '"""' if content.startswith('"""') else "'''"
            end_idx = content.find(delimiter, 3)
            if end_idx > 0:
                insert_idx = content[:end_idx + 3].count('\n')
        
        lines = content.split('\n')
        import_line = 'from modules.db_row_utils import _row_to_dict, _rows_to_dicts'
        lines.insert(insert_idx, import_line)
        lines.insert(insert_idx + 1, '')
        return '\n'.join(lines)


def inject_conversions(content):
    """
    Inject row/rows conversion calls after fetchone/fetchall.
    
    Pattern detection:
    - rows = cursor.fetchall() -> add: rows = _rows_to_dicts(rows)
    - row = cursor.fetchone() -> add: row = _row_to_dict(row)
    """
    lines = content.split('\n')
    new_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        new_lines.append(line)
        
        # Match patterns like: variable = something.fetchall()
        fetchall_match = re.search(r'(\w+)\s*=\s*.*\.fetchall\(\)', line)
        if fetchall_match:
            var_name = fetchall_match.group(1)
            indent = len(line) - len(line.lstrip())
            conversion = ' ' * indent + f'{var_name} = _rows_to_dicts({var_name})'
            new_lines.append(conversion)
        
        # Match patterns like: variable = something.fetchone()
        fetchone_match = re.search(r'(\w+)\s*=\s*.*\.fetchone\(\)', line)
        if fetchone_match:
            var_name = fetchone_match.group(1)
            indent = len(line) - len(line.lstrip())
            conversion = ' ' * indent + f'{var_name} = _row_to_dict({var_name})'
            new_lines.append(conversion)
        
        i += 1
    
    return '\n'.join(new_lines)


def create_diff(original_content, modified_content, filename):
    """Create a unified diff string."""
    original_lines = original_content.splitlines(keepends=True)
    modified_lines = modified_content.splitlines(keepends=True)
    
    diff = difflib.unified_diff(
        original_lines,
        modified_lines,
        fromfile=f'{filename}.orig',
        tofile=f'{filename}.fixed',
        lineterm=''
    )
    
    return ''.join(diff)


def process_file(filepath, dry_run=False):
    """
    Process a single file: create backup, inject conversions, create diff.
    
    Returns:
        tuple: (was_modified, message)
    """
    try:
        # Read the file
        with open(filepath, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        # Check if this file needs processing
        has_fetch = has_fetchall_or_fetchone(original_content)
        has_get = has_get_usage(original_content)
        
        if not (has_fetch and has_get):
            return False, "No fetch+get pattern detected"
        
        # Start with original content
        modified_content = original_content
        
        # Inject import if needed
        if needs_db_row_utils_import(modified_content):
            modified_content = inject_import(modified_content)
        
        # Inject conversions
        modified_content = inject_conversions(modified_content)
        
        # Check if anything actually changed
        if modified_content == original_content:
            return False, "No changes after processing"
        
        if dry_run:
            return True, "Would be modified (dry run)"
        
        # Create backup
        backup_path = filepath + '.bak'
        shutil.copy2(filepath, backup_path)
        
        # Write modified file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(modified_content)
        
        # Create diff file
        diff_content = create_diff(original_content, modified_content, os.path.basename(filepath))
        diff_path = filepath + '.fix.diff'
        with open(diff_path, 'w', encoding='utf-8') as f:
            f.write(diff_content)
        
        return True, f"Modified (backup: {backup_path}, diff: {diff_path})"
    
    except Exception as e:
        return False, f"Error: {e}"


def main():
    """Main function to run the auto-fix script."""
    # Determine base directory (repository root)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir)
    
    print("=" * 80)
    print("SQLite3 Row to Dict Auto-Fix Script")
    print("=" * 80)
    print(f"Base directory: {base_dir}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()
    
    # Check for dry-run mode
    dry_run = '--dry-run' in sys.argv or '-n' in sys.argv
    if dry_run:
        print("⚠ DRY RUN MODE - No files will be modified")
        print()
    
    # Find all Python files in modules/ and ui/
    python_files = find_python_files(base_dir)
    print(f"Found {len(python_files)} Python files in modules/ and ui/")
    print()
    
    # Process each file
    modified_count = 0
    skipped_count = 0
    error_count = 0
    
    for filepath in sorted(python_files):
        rel_path = os.path.relpath(filepath, base_dir)
        was_modified, message = process_file(filepath, dry_run)
        
        if was_modified:
            print(f"✓ {rel_path}: {message}")
            modified_count += 1
        elif 'Error' in message:
            print(f"✗ {rel_path}: {message}")
            error_count += 1
        else:
            # Skip silently or with verbose flag
            if '--verbose' in sys.argv or '-v' in sys.argv:
                print(f"- {rel_path}: {message}")
            skipped_count += 1
    
    # Print summary
    print()
    print("=" * 80)
    print("Summary")
    print("=" * 80)
    print(f"Modified: {modified_count}")
    print(f"Skipped:  {skipped_count}")
    print(f"Errors:   {error_count}")
    print()
    
    if not dry_run and modified_count > 0:
        print("⚠ Important:")
        print("  1. Review all .fix.diff files before committing")
        print("  2. Test the changes thoroughly")
        print("  3. Backups are available as .bak files")
        print("  4. To rollback, restore from .bak files")
        print()
    
    return 0 if error_count == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
