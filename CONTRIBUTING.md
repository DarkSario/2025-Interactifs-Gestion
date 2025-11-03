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
from modules.db_row_utils import _row_to_dict, _rows_to_dicts

# Single row
row = cursor.fetchone()
row_dict = _row_to_dict(row)
value = row_dict.get('column', default_value)

# Multiple rows
rows = cursor.fetchall()
rows_dicts = _rows_to_dicts(rows)
```

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
