#!/usr/bin/env python3
"""
Safe replacement script for centralizing exports package imports.

This script:
1. Detects import patterns that need to be replaced:
   - from exports.exports import X -> from exports import X
   - from modules.exports import X -> from exports import X
   - from exports.export_bilan_argumente import X -> from exports import X
2. Removes sys.path hacks around these imports
3. Adds TODO comments for automated changes
4. Runs in dry-run mode by default, requires --apply flag to make changes
"""

import os
import re
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Tuple, Set

# Exclusion patterns
EXCLUDE_DIRS = {'tests', 'venv', '.git', '__pycache__', '.pytest_cache', 'migrations'}
EXCLUDE_FILES = {'safe_replace_exports.py'}
EXCLUDE_PATTERNS = {
    'scripts/migration',
    'scripts/migrate_',
}
# Files that should NOT be modified (special cases)
EXCLUDE_SPECIFIC_FILES = {
    'exports/__init__.py',  # This IS the exports package, don't modify it
    'modules/exports.py',  # This is a shim layer, keep its structure
}

# Import patterns to replace
IMPORT_PATTERNS = [
    # Pattern 1: from exports.exports import X
    (
        r'from exports\.exports import (.+)',
        r'from exports import \1  # TODO: automated centralization change — see reports/TODOs.md'
    ),
    # Pattern 2: from modules.exports import X (EXCEPT ExportsWindow which is defined there)
    (
        r'from modules\.exports import (.+)',
        r'from exports import \1  # TODO: automated centralization change — see reports/TODOs.md'
    ),
    # Pattern 3: from exports.export_bilan_argumente import X
    (
        r'from exports\.export_bilan_argumente import (.+)',
        r'from exports import \1  # TODO: automated centralization change — see reports/TODOs.md'
    ),
]

# Items that should NOT be changed from modules.exports (they're defined there, not in exports)
MODULES_EXPORTS_EXCEPTIONS = {
    'ExportsWindow',
    'export_bilan_evenement',
    'export_depenses_global',
    'export_subventions_global',
    'export_tous_bilans_evenements',
}

# Sys.path hack patterns to detect and remove
SYSPATH_PATTERNS = [
    # Pattern: import sys, os ... parent_dir = ... sys.path.append(parent_dir)
    re.compile(
        r'(\s*)import sys,\s*os\s*\n'
        r'\1parent_dir = os\.path\.abspath\(os\.path\.join\(os\.path\.dirname\(__file__\),\s*[\'"]\.\.[\'\"]\)\)\s*\n'
        r'\1if parent_dir not in sys\.path:\s*\n'
        r'\1\s+sys\.path\.append\(parent_dir\)\s*\n',
        re.MULTILINE
    ),
    # Pattern: sys.path.insert(0, ...)
    re.compile(
        r'(\s*)sys\.path\.insert\(0,\s*[^\)]+\)\s*\n',
        re.MULTILINE
    ),
]


def should_exclude_file(file_path: Path, repo_root: Path) -> bool:
    """Check if a file should be excluded from processing."""
    rel_path = file_path.relative_to(repo_root)
    rel_path_str = str(rel_path)
    
    # Check if file is specifically excluded
    for excluded in EXCLUDE_SPECIFIC_FILES:
        if rel_path_str == excluded or rel_path_str.replace('\\', '/') == excluded:
            return True
    
    # Check if file is in excluded directory
    for part in rel_path.parts:
        if part in EXCLUDE_DIRS:
            return True
    
    # Check if file matches excluded filename
    if file_path.name in EXCLUDE_FILES:
        return True
    
    # Check if file matches excluded patterns
    for pattern in EXCLUDE_PATTERNS:
        if pattern in rel_path_str:
            return True
    
    return False


def find_python_files(repo_root: Path) -> List[Path]:
    """Find all Python files to process."""
    python_files = []
    for py_file in repo_root.rglob('*.py'):
        if not should_exclude_file(py_file, repo_root):
            python_files.append(py_file)
    return sorted(python_files)


def detect_import_changes(content: str) -> List[Tuple[str, str, int]]:
    """
    Detect import patterns that need to be changed.
    Returns list of (old_line, new_line, line_number) tuples.
    """
    changes = []
    lines = content.split('\n')
    
    for line_num, line in enumerate(lines, 1):
        for pattern, replacement in IMPORT_PATTERNS:
            match = re.match(r'^' + pattern + r'$', line.strip())
            if match:
                # Check if line already has a TODO comment
                if '# TODO: automated centralization change' not in line:
                    # Special handling for modules.exports imports
                    if 'from modules.exports import' in line:
                        # Extract what's being imported
                        import_match = re.search(r'from modules\.exports import (.+)', line)
                        if import_match:
                            imports = import_match.group(1).strip()
                            # Check if it's a parenthesized import
                            if imports.startswith('('):
                                # Multi-line import, skip for now (would need more complex handling)
                                continue
                            # Check if any exception is in the imports
                            skip = False
                            for exception in MODULES_EXPORTS_EXCEPTIONS:
                                if exception in imports:
                                    skip = True
                                    break
                            if skip:
                                continue
                    
                    new_line = re.sub(pattern, replacement, line.strip())
                    changes.append((line, new_line, line_num))
                    break
    
    return changes


def detect_syspath_hacks(content: str) -> List[Tuple[str, int, int]]:
    """
    Detect sys.path hacks that should be removed.
    Returns list of (hack_text, start_line, end_line) tuples.
    """
    hacks = []
    lines = content.split('\n')
    
    for pattern in SYSPATH_PATTERNS:
        for match in pattern.finditer(content):
            start_pos = match.start()
            end_pos = match.end()
            
            # Calculate line numbers
            start_line = content[:start_pos].count('\n') + 1
            end_line = content[:end_pos].count('\n') + 1
            
            hack_text = match.group(0)
            hacks.append((hack_text, start_line, end_line))
    
    return hacks


def apply_changes(file_path: Path, dry_run: bool = True) -> Dict:
    """
    Apply changes to a file (or simulate in dry-run mode).
    Returns dict with change information.
    """
    result = {
        'file': str(file_path),
        'import_changes': [],
        'syspath_hacks': [],
        'modified': False,
        'error': None
    }
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        # Detect import changes
        import_changes = detect_import_changes(original_content)
        result['import_changes'] = [(old, new, line) for old, new, line in import_changes]
        
        # Detect sys.path hacks
        syspath_hacks = detect_syspath_hacks(original_content)
        result['syspath_hacks'] = [(text, start, end) for text, start, end in syspath_hacks]
        
        if not import_changes and not syspath_hacks:
            return result
        
        # Apply changes
        new_content = original_content
        
        # Replace imports
        for old_line, new_line, _ in import_changes:
            new_content = new_content.replace(old_line, new_line)
        
        # Remove sys.path hacks (process in reverse order to maintain line numbers)
        for hack_text, _, _ in sorted(syspath_hacks, key=lambda x: x[1], reverse=True):
            new_content = new_content.replace(hack_text, '')
        
        if not dry_run:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            result['modified'] = True
        
    except Exception as e:
        result['error'] = str(e)
    
    return result


def generate_report(results: List[Dict], output_file: Path):
    """Generate a markdown report of all changes."""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Exports Centralization Report\n\n")
        f.write("This report shows all files that were analyzed for exports import centralization.\n\n")
        
        # Summary statistics
        total_files = len(results)
        files_with_changes = sum(1 for r in results if r['import_changes'] or r['syspath_hacks'])
        total_import_changes = sum(len(r['import_changes']) for r in results)
        total_syspath_removals = sum(len(r['syspath_hacks']) for r in results)
        files_with_errors = sum(1 for r in results if r['error'])
        
        f.write("## Summary\n\n")
        f.write(f"- Total files analyzed: {total_files}\n")
        f.write(f"- Files with changes: {files_with_changes}\n")
        f.write(f"- Total import changes: {total_import_changes}\n")
        f.write(f"- Total sys.path hacks removed: {total_syspath_removals}\n")
        f.write(f"- Files with errors: {files_with_errors}\n\n")
        
        # Files with changes
        if files_with_changes > 0:
            f.write("## Files Modified\n\n")
            for result in results:
                if result['import_changes'] or result['syspath_hacks']:
                    f.write(f"### {result['file']}\n\n")
                    
                    if result['import_changes']:
                        f.write("**Import Changes:**\n\n")
                        for old, new, line_num in result['import_changes']:
                            f.write(f"Line {line_num}:\n")
                            f.write(f"- Before: `{old.strip()}`\n")
                            f.write(f"- After: `{new.strip()}`\n\n")
                    
                    if result['syspath_hacks']:
                        f.write("**Sys.path Hacks Removed:**\n\n")
                        for hack, start, end in result['syspath_hacks']:
                            f.write(f"Lines {start}-{end}:\n")
                            f.write("```python\n")
                            f.write(hack)
                            f.write("```\n\n")
        
        # Errors
        if files_with_errors > 0:
            f.write("## Files with Errors\n\n")
            for result in results:
                if result['error']:
                    f.write(f"- {result['file']}: {result['error']}\n")
            f.write("\n")


def generate_candidates_report(results: List[Dict], output_file: Path):
    """Generate a report of files that are candidates for automated changes."""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Exports Centralization Candidates\n\n")
        f.write("This report lists files that contain imports that can be automatically centralized.\n\n")
        
        candidates = [r for r in results if r['import_changes'] or r['syspath_hacks']]
        
        if candidates:
            f.write("## Candidate Files\n\n")
            for result in candidates:
                f.write(f"- `{result['file']}`\n")
                if result['import_changes']:
                    f.write(f"  - {len(result['import_changes'])} import(s) to centralize\n")
                if result['syspath_hacks']:
                    f.write(f"  - {len(result['syspath_hacks'])} sys.path hack(s) to remove\n")
            f.write(f"\n**Total candidates:** {len(candidates)}\n\n")
        else:
            f.write("No candidates found.\n\n")


def main():
    parser = argparse.ArgumentParser(
        description='Safely replace exports imports to centralize them'
    )
    parser.add_argument(
        '--apply',
        action='store_true',
        help='Apply changes (default is dry-run mode)'
    )
    parser.add_argument(
        '--report',
        type=str,
        default='reports/EXPORTS_CENTRALIZATION_REPORT.md',
        help='Output report file path'
    )
    
    args = parser.parse_args()
    
    # Get repository root
    repo_root = Path(__file__).parent.parent
    
    print(f"{'=' * 70}")
    print(f"Exports Import Centralization Script")
    print(f"{'=' * 70}")
    print(f"Mode: {'APPLY' if args.apply else 'DRY-RUN'}")
    print(f"Repository: {repo_root}")
    print(f"{'=' * 70}\n")
    
    # Find Python files
    print("Finding Python files...")
    python_files = find_python_files(repo_root)
    print(f"Found {len(python_files)} Python files to analyze\n")
    
    # Process files
    print("Analyzing files...")
    results = []
    for file_path in python_files:
        result = apply_changes(file_path, dry_run=not args.apply)
        results.append(result)
        
        if result['import_changes'] or result['syspath_hacks']:
            print(f"  📝 {file_path.relative_to(repo_root)}")
            if result['import_changes']:
                print(f"     → {len(result['import_changes'])} import(s)")
            if result['syspath_hacks']:
                print(f"     → {len(result['syspath_hacks'])} sys.path hack(s)")
    
    print()
    
    # Generate reports
    reports_dir = repo_root / 'reports'
    reports_dir.mkdir(exist_ok=True)
    
    report_file = repo_root / args.report
    print(f"Generating report: {report_file}")
    generate_report(results, report_file)
    
    candidates_file = reports_dir / 'EXPORTS_CENTRALIZATION_CANDIDATES.md'
    print(f"Generating candidates report: {candidates_file}")
    generate_candidates_report(results, candidates_file)
    
    # Summary
    files_with_changes = sum(1 for r in results if r['import_changes'] or r['syspath_hacks'])
    total_import_changes = sum(len(r['import_changes']) for r in results)
    total_syspath_removals = sum(len(r['syspath_hacks']) for r in results)
    
    print(f"\n{'=' * 70}")
    print(f"Summary")
    print(f"{'=' * 70}")
    print(f"Files analyzed: {len(results)}")
    print(f"Files with changes: {files_with_changes}")
    print(f"Import changes: {total_import_changes}")
    print(f"Sys.path hacks removed: {total_syspath_removals}")
    print(f"{'=' * 70}")
    
    if not args.apply:
        print("\n⚠️  DRY-RUN MODE: No files were modified.")
        print("   Run with --apply to apply changes.\n")
    else:
        print(f"\n✅ Changes applied to {files_with_changes} file(s).\n")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
