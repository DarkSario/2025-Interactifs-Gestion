# Contribution

Merci de votre intérêt pour contribuer à ce dépôt. Quelques règles simples :

- Ouvrir une issue pour discuter les changements importants.
- Faire une branche par fonctionnalité : `git checkout -b feat/ma-fonctionnalite`
- Respecter le style du code (utiliser black/flake8 si configurés).
- Ajouter ou mettre à jour les tests pour toute fonctionnalité ou correction de bug.
- Ouvrir une pull request ciblant la branche `main`.

Exemples de commandes :

```bash
git checkout -b feat/ma-fonctionnalite
git add .
git commit -m "feat: description"
git push origin feat/ma-fonctionnalite
```

## Database Access Patterns

When working with the database, follow these best practices:

### 1. Always Use the Unified API

**❌ Don't use direct sqlite3.connect():**
```python
import sqlite3
conn = sqlite3.connect("association.db")  # Missing WAL and busy_timeout
```

**✅ Use get_connection():**
```python
from db.db import get_connection
conn = get_connection()  # WAL mode and busy_timeout configured
```

### 2. Use Transactions for Writes

**❌ Don't use separate statements:**
```python
conn = get_connection()
cursor = conn.cursor()
cursor.execute("INSERT INTO ...")
cursor.execute("UPDATE ...")
conn.commit()
```

**✅ Use transaction context manager:**
```python
from src.db.connection import connect, transaction

conn = connect()
with transaction(conn) as cur:
    cur.execute("INSERT INTO ...")
    cur.execute("UPDATE ...")
# Automatically commits or rolls back
conn.close()
```

### 3. Convert Rows to Dicts for .get() Access

Rows returned by queries are `sqlite3.Row` objects. Convert them to dicts to use `.get()`:

```python
# Preferred: Use src.db.row_utils (centralized utilities)
from src.db.row_utils import row_to_dict, rows_to_dicts

# Single row
row = cursor.fetchone()
row_dict = row_to_dict(row)
value = row_dict.get('column', default_value)

# Multiple rows
rows = cursor.fetchall()
rows_dicts = rows_to_dicts(rows)

# Alternative: modules.db_row_utils (legacy, for backward compatibility)
from modules.db_row_utils import _row_to_dict, _rows_to_dicts
# Or from utils.db_helpers import row_to_dict, rows_to_dicts
```

**Why this matters:** `sqlite3.Row` objects do not have a `.get()` method. Using `.get()` on a Row will raise `AttributeError`. Always convert to dict first.

### 4. Use Service Classes for Domain Logic

Instead of writing SQL in UI or business logic:

```python
# ❌ Don't
cursor.execute("SELECT * FROM buvette_inventaire_lignes WHERE inventaire_id = ?", (id,))

# ✅ Do
from src.services.inventory_service import InventoryService
service = InventoryService()
lines = service.load_inventory_lines(inventory_id)
```

### 5. Use File Locks for Critical Operations

For operations that must not run concurrently:

```python
from src.db.lock import db_file_lock

with db_file_lock(db_path):
    # Critical section - exclusive access
    service.create_inventory(metadata)
```

### 6. Close Connections Promptly

Always close connections when done:

```python
conn = get_connection()
try:
    # ... use connection
finally:
    conn.close()
```

## Testing

Run tests before submitting a PR:

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_inventory_service.py -v

# Run with coverage
python -m pytest tests/ --cov=. --cov-report=html
```

## Documentation

- See [docs/DB_GUIDE.md](docs/DB_GUIDE.md) for comprehensive database API documentation
- Update documentation when adding new features or changing APIs
- Add docstrings to all public functions and classes

## Code Review Checklist

Before submitting your PR, verify:

- [ ] All tests pass
- [ ] No direct `sqlite3.connect()` calls (use `get_connection()`)
- [ ] Transactions use `transaction()` context manager
- [ ] Rows converted to dicts before `.get()` access
- [ ] Service classes used for domain logic
- [ ] Connections closed properly
- [ ] Documentation updated
- [ ] Commit messages follow conventional commits format

## Audit and Safety Scripts

Before making database changes, run these scripts to identify potential issues:

### 1. Database Usage Audit

Scan the entire codebase for database access patterns:

```bash
python scripts/audit_db_usage.py
```

This generates:
- `reports/SQL_ACCESS_MAP.md` - Maps all database access patterns
- `reports/TODOs.md` - Lists action items for fixing issues

### 2. Row.get() Pattern Detection

Identify unsafe `.get()` usage on sqlite3.Row objects:

```bash
# Dry-run: Show potential issues
python scripts/replace_row_get.py

# Check specific file
python scripts/replace_row_get.py --file modules/buvette_db.py

# Apply fixes automatically (use with caution)
python scripts/replace_row_get.py --apply
```

**⚠️ Important:** Always run in dry-run mode first and review the suggested changes before applying.

### 3. Connection Standardization

Find direct `sqlite3.connect()` calls that should use `get_connection()`:

```bash
# Dry-run: List files with direct connections
python scripts/replace_sqlite_connect.py

# Apply fixes to specific file
python scripts/replace_sqlite_connect.py --file path/to/file.py --apply
```

### 4. Buvette Module Verification

Run comprehensive checks on the buvette module:

```bash
python scripts/check_buvette.py
```

This verifies:
- Database schema compliance
- SQL query patterns
- UI implementation
- Test suite status

### Safety Guidelines for Database Changes

**Before making changes:**
1. ✅ Backup the database: `cp db/association.db db/association.db.backup`
2. ✅ Run audit scripts in dry-run mode
3. ✅ Review generated reports in `reports/` directory
4. ✅ Test changes on a copy of the database first
5. ✅ Run all tests: `python -m pytest tests/`

**When applying automated fixes:**
1. ✅ Run scripts with dry-run first (without `--apply`)
2. ✅ Review each suggested change carefully
3. ✅ Apply changes selectively, not globally
4. ✅ Test thoroughly after each change
5. ✅ Commit changes in small, atomic commits

**For structural migrations:**
1. ❌ Do NOT drop or rename columns without thorough review
2. ❌ Do NOT apply automated replacements to tests or scripts without verification
3. ✅ Create candidate lists for manual review (see `reports/COLUMN_REMOVAL_CANDIDATES.md`)
4. ✅ Use non-destructive migrations that add columns, not remove them
5. ✅ Maintain backward compatibility with SELECT aliases

### Reports Directory

The `reports/` directory contains:
- `SQL_ACCESS_MAP.md` - Complete map of database access patterns
- `TODOs.md` - Prioritized action items for code improvements
- `buvette_AUDIT.md` - Comprehensive audit of buvette module
- `COLUMN_REMOVAL_CANDIDATES.md` - Columns that may need review (manual only)
