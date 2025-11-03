# Stock Management & Articles Migration Guide

## Overview

This guide documents the stock management system and articles migration implemented in PR #XX (branch: fix/stock-and-unite).

## Features Implemented

### 1. Stock Journal System

A comprehensive stock tracking system with audit trail capabilities:

- **inventory_stock_journal table**: Records all stock changes from inventories
- **Transactional operations**: All stock changes are atomic and reversible
- **Audit trail**: Every inventory creates journal entries for revert capability

### 2. Automatic Stock Management

Stock is automatically updated when:

1. **Creating an inventory**: Stock is set to inventory quantities
2. **Deleting an inventory**: Stock changes are reverted using journal
3. **Creating a purchase (achat)**: Stock increases by purchase quantity
4. **Deleting a purchase**: Stock decreases by purchase quantity

### 3. Articles Schema Migration

Migration from text-based `unite` to structured schema:

**Old Schema:**
```sql
CREATE TABLE buvette_articles (
    id INTEGER PRIMARY KEY,
    name TEXT,
    unite TEXT,  -- "piece", "litre", etc.
    ...
)
```

**New Schema:**
```sql
CREATE TABLE buvette_articles (
    id INTEGER PRIMARY KEY,
    name TEXT,
    quantite INTEGER DEFAULT 0,  -- NEW: numeric quantity
    unite_type TEXT,              -- NEW: preserves old unite value
    ...
)
```

### 4. Backward Compatibility

A compatibility view ensures existing code continues to work:

```sql
CREATE VIEW buvette_articles_compat AS
SELECT 
    id,
    name,
    COALESCE(unite_type, '') AS unite,  -- Exposes unite for legacy code
    ...
FROM buvette_articles
```

## Migration Steps

### Prerequisites

1. **Backup your database** (mandatory):
```bash
cp association.db association.db.backup-$(date +%Y%m%d-%H%M%S)
```

2. **Stop the application** if running

### Step 1: Migrate Articles Table

```bash
python scripts/migrate_articles_unite_to_quantite.py --db association.db
```

This script:
- Creates an automatic `.bak` backup
- Recreates `buvette_articles` with new schema
- Copies all data (unite → unite_type)
- Preserves stock and all other columns

**Verification:**
```bash
sqlite3 association.db "PRAGMA table_info(buvette_articles);"
```

Expected columns: id, name, categorie, quantite, unite_type, contenance, commentaire, stock, purchase_price

### Step 2: Create Compatibility Views

```bash
python scripts/create_compat_views.py --db association.db
```

This script:
- Creates `buvette_articles_compat` view
- Exposes `unite` column for legacy code

**Verification:**
```bash
sqlite3 association.db "SELECT name FROM sqlite_master WHERE type='view' AND name='buvette_articles_compat';"
```

### Step 3: Start Application

```bash
python main.py
```

The application will automatically:
- Create `inventory_stock_journal` table if missing
- Initialize stock management system

**Verification:**
```bash
sqlite3 association.db "SELECT name FROM sqlite_master WHERE type='table' AND name='inventory_stock_journal';"
```

## Testing

Run the test suite to verify migration:

```bash
# All stock-related tests
python -m pytest tests/test_stock_journal.py tests/test_delete_inventaire.py tests/test_buvette_stock.py -v

# Expected: All tests pass ✅
```

## Usage Examples

### Python API

```python
from modules.stock_db import get_stock, adjust_stock, apply_inventory_snapshot

# Get current stock
stock = get_stock(article_id=1)

# Adjust stock manually
adjust_stock(article_id=1, delta=10, reason="Manual adjustment")

# Apply inventory snapshot (usually automatic)
snapshot = [
    {"article_id": 1, "quantite": 50},
    {"article_id": 2, "quantite": 30}
]
apply_inventory_snapshot(inv_id=1, snapshot=snapshot)
```

### SQL Queries

```sql
-- Get stock for all articles
SELECT id, name, stock FROM buvette_articles ORDER BY name;

-- Get stock journal for an inventory
SELECT * FROM inventory_stock_journal WHERE inventaire_id = 1;

-- Use compatibility view (legacy code)
SELECT id, name, unite FROM buvette_articles_compat;
```

## Troubleshooting

### Migration Failed

If migration fails:
1. Restore from backup: `cp association.db.backup-YYYYMMDD-HHMMSS association.db`
2. Check error message in console
3. Verify database is not in use

### Stock Inconsistencies

If stock values seem incorrect:
1. Check `inventory_stock_journal` table for audit trail
2. Verify inventory lines are correct
3. Re-run inventory to recalculate stock

### Compatibility Issues

If legacy code doesn't work after migration:
1. Ensure `create_compat_views.py` was run
2. Use `buvette_articles_compat` view instead of table
3. Or update code to use `unite_type` column

## Technical Details

### Stock Journal Schema

```sql
CREATE TABLE inventory_stock_journal (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    inventaire_id INTEGER NOT NULL,
    article_id INTEGER NOT NULL,
    delta INTEGER NOT NULL,
    date_created TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (inventaire_id) REFERENCES buvette_inventaires(id),
    FOREIGN KEY (article_id) REFERENCES buvette_articles(id)
)
```

### Functions Available

#### modules/stock_db.py
- `ensure_stock_tables()` - Create journal table if missing
- `get_stock(article_id)` - Get current stock
- `set_stock(article_id, qty)` - Set absolute stock value
- `adjust_stock(article_id, delta, reason=None)` - Adjust stock by delta
- `apply_inventory_snapshot(inv_id, snapshot)` - Apply inventory and record deltas
- `revert_inventory_effect(inv_id)` - Revert inventory changes
- `inventory_stock_journal(inv_id)` - Get journal entries for inventory

#### modules/buvette_inventaire_db.py
- `apply_inventory_snapshot_wrapper(inv_id)` - Helper for UI flows
- `delete_inventaire(inv_id)` - Delete with automatic stock revert

#### modules/stock_tab.py
- `get_stock_listing()` - Get all articles with stock for UI

## Files Modified

- `main.py` - Added stock tables initialization at startup
- `modules/buvette_db.py` - Stock adjustments in achats create/delete
- `modules/buvette_inventaire_dialogs.py` - Inventory snapshot application
- `scripts/create_compat_views.py` - NEW: Compatibility views script

## Files Already Present (No Changes)

- `modules/stock_db.py` - Stock management functions
- `modules/stock_tab.py` - Stock UI helper
- `modules/buvette_inventaire_db.py` - Inventory DB with revert support
- `scripts/migrate_articles_unite_to_quantite.py` - Articles migration script
- `tests/test_stock_journal.py` - Stock journal tests
- `tests/test_delete_inventaire.py` - Inventory deletion tests

## Support

For issues or questions:
1. Check this guide first
2. Review test files for usage examples
3. Check logs in application console
4. Create an issue on GitHub

## Rollback

To rollback the migration:

```bash
# 1. Stop the application
# 2. Restore from backup
cp association.db.backup-YYYYMMDD-HHMMSS association.db
# 3. Restart application
python main.py
```

Note: Rollback will lose any data created after migration.
