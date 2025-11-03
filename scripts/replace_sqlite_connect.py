"""AST-based replacer: replace sqlite3.connect(...) with get_connection(...)

Run from repo root:
python scripts/replace_sqlite_connect.py --apply

This script adds an import for get_connection from src.db.compat when it modifies a file.
"""
import ast
import astor
import sys
from pathlib import Path
import argparse

IGNOREFILES = ["venv", ".venv", ".git", "__pycache__", "tests"]
# Also skip migration scripts and critical DB infrastructure that must remain raw
SKIP_PATTERNS = ["migration", "migrate_", "db_diagnostics", "enable_wal", "update_db_structure", "create_compat_views"]
# Skip files that define get_connection (they need sqlite3.connect internally)
SKIP_FILES = {"db/db.py", "modules/db_api.py", "src/db/compat.py", "src/db/connection.py"}

def should_skip(p: Path):
    for x in IGNOREFILES:
        if x in p.parts:
            return True
    # Skip files matching skip patterns (migrations, diagnostics, etc.)
    for pattern in SKIP_PATTERNS:
        if pattern in p.name:
            return True
    # Skip specific files that define get_connection - check string path
    path_str = str(p)
    for skip_file in SKIP_FILES:
        if path_str.endswith(skip_file) or skip_file in path_str:
            return True
    return False

class ConnectRewriter(ast.NodeTransformer):
    def __init__(self):
        super().__init__()
        self.need_import = False

    def visit_Call(self, node):
        # match sqlite3.connect(...)
        if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
            if node.func.value.id == "sqlite3" and node.func.attr == "connect":
                # replace by get_connection(...)
                self.need_import = True
                new = ast.Call(func=ast.Name(id="get_connection", ctx=ast.Load()), args=node.args, keywords=node.keywords)
                return ast.copy_location(new, node)
        return self.generic_visit(node)

def process_file(path: Path, apply_changes: bool):
    src = path.read_text(encoding="utf-8")
    try:
        tree = ast.parse(src)
    except Exception:
        return False, False
    rewriter = ConnectRewriter()
    tree2 = rewriter.visit(tree)
    ast.fix_missing_locations(tree2)
    if not rewriter.need_import:
        return False, False
    src2 = astor.to_source(tree2)
    # Ensure import get_connection present
    if "get_connection" not in src2.splitlines()[0:40]:
        import_line = "from src.db.compat import get_connection\n"
        src2 = import_line + src2
    if apply_changes:
        path.write_text(src2, encoding="utf-8")
    return True, True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Apply changes")
    args = parser.parse_args()
    root = Path(".")
    files = list(root.rglob("*.py"))
    changed = []
    for f in files:
        if should_skip(f):
            continue
        ok, modified = process_file(f, args.apply)
        if ok:
            changed.append(str(f))
    print("Files with sqlite3.connect replaced:", len(changed))
    for c in changed:
        print(" -", c)
    if not args.apply:
        print("\nRun with --apply to modify files.")

if __name__ == "__main__":
    main()
