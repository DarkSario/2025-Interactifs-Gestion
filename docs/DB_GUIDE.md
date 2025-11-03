# Database Access Guide

This guide explains the unified database access API and best practices for working with the SQLite database in this project.

## Overview

The project uses a unified database access layer that ensures:
- **WAL mode** (Write-Ahead Logging) for better concurrency
- **Busy timeout** (5 seconds) to reduce "Database locked" errors
- **Consistent row factory** (sqlite3.Row) for named column access
- **Centralized configuration** via APP_DB_PATH environment variable

## Quick Start

### Basic Connection

```python
from db.db import get_connection

# Get a connection with WAL mode and busy_timeout already configured
conn = get_connection()
cursor = conn.cursor()
cursor.execute("SELECT * FROM articles WHERE id = ?", (article_id,))
row = cursor.fetchone()
conn.close()
```

### Using the New API

For new code, prefer using the `src.db.connection` module:

```python
from src.db.connection import connect, transaction

# Get a connection
conn = connect()

# Use transaction context manager for writes
with transaction(conn) as cur:
    cur.execute("INSERT INTO articles (name) VALUES (?)", ("Coffee",))
    cur.execute("UPDATE stock SET qty = qty - 1 WHERE id = ?", (1,))
# Automatically commits if no exception, rolls back on error

conn.close()
```

### Using Services

For high-level operations, use service classes:

```python
from src.services.inventory_service import InventoryService

service = InventoryService()

# Load inventory lines (automatically detects schema)
lines = service.load_inventory_lines(inventory_id=42)
for line in lines:
    print(f"Product {line['product_id']}: qty {line['qty']}")

# Create inventory with file lock (prevents race conditions)
new_id = service.create_inventory({"name": "Monthly inventory"})
```

## API Reference

### Legacy API (db.db)

The legacy `db.db` module provides backward compatibility:

```python
from db.db import get_connection, set_db_file, get_db_file

# Get/set the database file path
current_path = get_db_file()
set_db_file("/path/to/my.db")  # Also sets APP_DB_PATH env var

# Get a connection (delegates to src.db.connection.connect)
conn = get_connection()
```

### New API (src.db.connection)

```python
from src.db.connection import connect, transaction, set_busy_timeout

# Connect with custom path
conn = connect(db_path="/path/to/db.sqlite", timeout=10.0)

# Transaction context manager
with transaction(conn) as cur:
    cur.execute("INSERT INTO table (col) VALUES (?)", (value,))

# Adjust busy timeout on live connection
set_busy_timeout(conn, ms=10000)
```

### File Locking (src.db.lock)

For operations that must not run concurrently (e.g., schema changes):

```python
from src.db.lock import db_file_lock
from pathlib import Path

db_path = Path("association.db")

with db_file_lock(db_path):
    # Exclusive operations here
    # Other processes will wait for the lock
    conn = connect(db_path)
    # ... perform migration or critical writes
    conn.close()
```

## Configuration

### Database Path

The database path is configured via the `APP_DB_PATH` environment variable:

1. **Set in main.py** (before importing DB modules):
   ```python
   import os
   os.environ["APP_DB_PATH"] = "association.db"
   ```

2. **Or via set_db_file()**:
   ```python
   from db.db import set_db_file
   set_db_file("/path/to/db.sqlite")
   ```

Priority order:
1. `APP_DB_PATH` environment variable
2. Legacy `DB_FILE` environment variable (if set)
3. Default: `association.db`

### Busy Timeout

Default busy timeout is 5000ms (5 seconds). Configure via:

- `DB_BUSY_TIMEOUT_MS` environment variable (for src.db.connection)
- `PRAGMA busy_timeout` is automatically set by `get_connection()`

## Best Practices

### 1. Use get_connection() for All Database Access

❌ **Don't:**
```python
import sqlite3
conn = sqlite3.connect("association.db")  # Missing WAL, busy_timeout
```

✅ **Do:**
```python
from db.db import get_connection
conn = get_connection()  # WAL and busy_timeout configured
```

### 2. Use Transactions for Multi-Statement Writes

❌ **Don't:**
```python
conn = get_connection()
cursor = conn.cursor()
cursor.execute("INSERT INTO ...")
cursor.execute("UPDATE ...")
conn.commit()  # Separate statements not atomic
```

✅ **Do:**
```python
from src.db.connection import connect, transaction

conn = connect()
with transaction(conn) as cur:
    cur.execute("INSERT INTO ...")
    cur.execute("UPDATE ...")
# Atomic commit on success, rollback on exception
```

### 3. Convert Rows to Dicts for .get() Access

Rows are `sqlite3.Row` objects, which support `row['column']` but not `row.get('column')`:

```python
from modules.db_row_utils import _row_to_dict, _rows_to_dicts

# Single row
row = cursor.fetchone()
row_dict = _row_to_dict(row)
value = row_dict.get('column', default_value)

# Multiple rows
rows = cursor.fetchall()
rows_dicts = _rows_to_dicts(rows)
for row_dict in rows_dicts:
    value = row_dict.get('column', default_value)
```

### 4. Use Services for Domain Logic

Instead of writing SQL everywhere, use or create service classes:

```python
# ❌ Don't scatter SQL throughout the codebase
conn = get_connection()
cursor = conn.cursor()
cursor.execute("SELECT * FROM buvette_inventaire_lignes WHERE inventaire_id = ?", (inv_id,))
# ... complex logic

# ✅ Use a service
from src.services.inventory_service import InventoryService
service = InventoryService()
lines = service.load_inventory_lines(inv_id)
```

### 5. Use File Locks for Critical Operations

For operations that create schema or perform multi-step writes across processes:

```python
from src.db.lock import db_file_lock

with db_file_lock(db_path):
    # Critical section - only one process at a time
    service.create_inventory(metadata)
```

## Schema Compatibility

`InventoryService` automatically detects legacy schema names:

| Concept | New Schema | Legacy Schema |
|---------|------------|---------------|
| Inventory lines table | `inventory_lines` | `inventaire_lignes` or `buvette_inventaire_lignes` |
| Product/Article ID | `product_id` | `article_id` or `stock_id` |
| Quantity | `qty` | `quantite` or `quantite_constatee` |

This allows the code to work with both old and new database schemas.

## Troubleshooting

### "Database is locked" Errors

**Causes:**
- Concurrent writes without WAL mode
- Missing busy_timeout configuration
- Long-running transactions holding locks

**Solutions:**
1. Ensure all code uses `get_connection()` (not direct `sqlite3.connect()`)
2. Use `transaction()` context manager for writes
3. Use `db_file_lock()` for critical operations
4. Close connections promptly

### Empty Reads

**Causes:**
- Uncommitted transactions in other connections
- Missing WAL mode

**Solutions:**
1. Use `get_connection()` to ensure WAL mode
2. Commit or rollback transactions promptly
3. Use `transaction()` context manager

### Row Attribute Errors

**Cause:**
- Using `row.get('column')` on `sqlite3.Row` objects

**Solution:**
- Convert to dict first: `row_dict = _row_to_dict(row)`

## Migration Path

The project uses a **compatibility shim** approach:

1. **Phase 1 (Current):** Both APIs coexist
   - Legacy `db.db.get_connection()` delegates to new API
   - Both work transparently

2. **Phase 2 (Future):** Gradual migration
   - Update modules to import from `src.db.connection` directly
   - Replace direct SQL with service classes

3. **Phase 3 (Final):** Remove legacy API
   - Remove `db.db` compatibility layer
   - All code uses `src.db.*` directly

## Examples

### Example 1: Query with Error Handling

```python
from db.db import get_connection
from modules.db_row_utils import _rows_to_dicts

def get_articles_by_category(category):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM buvette_articles WHERE categorie = ? ORDER BY name",
            (category,)
        )
        rows = cursor.fetchall()
        return _rows_to_dicts(rows)
    except Exception as e:
        logger.error(f"Error loading articles: {e}")
        raise
    finally:
        if conn:
            conn.close()
```

### Example 2: Transaction with Rollback

```python
from src.db.connection import connect, transaction

def transfer_stock(from_id, to_id, quantity):
    conn = connect()
    try:
        with transaction(conn) as cur:
            # Deduct from source
            cur.execute(
                "UPDATE buvette_articles SET stock = stock - ? WHERE id = ?",
                (quantity, from_id)
            )
            # Add to destination
            cur.execute(
                "UPDATE buvette_articles SET stock = stock + ? WHERE id = ?",
                (quantity, to_id)
            )
            # Both succeed or both fail atomically
        return True
    except Exception as e:
        logger.error(f"Transfer failed: {e}")
        return False
    finally:
        conn.close()
```

### Example 3: File-Locked Critical Operation

```python
from src.db.connection import connect, transaction, DB_DEFAULT_PATH
from src.db.lock import db_file_lock

def create_year_end_snapshot():
    db_path = DB_DEFAULT_PATH
    with db_file_lock(db_path):
        # Only one process can do this at a time
        conn = connect()
        try:
            with transaction(conn) as cur:
                # Create snapshot table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS year_end_snapshot (
                        id INTEGER PRIMARY KEY,
                        year INTEGER,
                        data TEXT
                    )
                """)
                # Insert data
                cur.execute(
                    "INSERT INTO year_end_snapshot (year, data) VALUES (?, ?)",
                    (2024, "snapshot data")
                )
        finally:
            conn.close()
```

## Additional Resources

- [SQLite WAL Mode](https://www.sqlite.org/wal.html)
- [SQLite Busy Timeout](https://www.sqlite.org/c3ref/busy_timeout.html)
- [Python sqlite3 Module](https://docs.python.org/3/library/sqlite3.html)

## Support

For questions or issues:
1. Check this guide
2. Review the code in `db/db.py` and `src/db/`
3. Open an issue on GitHub
