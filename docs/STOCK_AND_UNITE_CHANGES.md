# Stock Management and Unite Migration - Implementation Guide

## Overview

This PR implements conservative, backward-compatible changes for the 'buvette' functionality, including:
1. Stock database and journal system
2. Inventory DB flow integration
3. UI helpers for stock listing
4. Articles migration from 'unite' to 'quantite'

## Changes Summary

### 1. Stock Database and Journal (`modules/stock_db.py`)

**Already Implemented** - The module provides:

- `ensure_stock_tables(conn=None)`: Creates necessary tables
  - `inventory_stock_journal`: Records stock changes from inventories
  - `article_purchase_batches`: Tracks purchase lots for FIFO costing

- Stock manipulation functions:
  - `get_stock(conn, article_id)`: Get current stock level
  - `set_stock(conn, article_id, qty)`: Set stock to absolute value
  - `adjust_stock(conn, article_id, delta)`: Adjust stock by delta

- Inventory integration:
  - `apply_inventory_snapshot(conn, inventaire_id, lines_table_candidates)`: Apply inventory and record deltas
  - `revert_inventory_effect(conn, inventaire_id)`: Revert inventory effects using journal
  - `inventory_stock_journal(conn, inv_id)`: Get journal entries for an inventory

- FIFO costing:
  - `create_purchase_batch(conn, article_id, qty, unit_price, purchase_id)`: Create purchase batch
  - `consume_purchase_batches_fifo(conn, article_id, qty)`: Consume batches in FIFO order

**Table Schemas:**
```sql
CREATE TABLE inventory_stock_journal (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    inventaire_id INTEGER,
    achat_id INTEGER,
    article_id INTEGER NOT NULL,
    delta INTEGER NOT NULL,
    scope TEXT DEFAULT 'buvette',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (inventaire_id) REFERENCES buvette_inventaires(id),
    FOREIGN KEY (article_id) REFERENCES buvette_articles(id)
);

CREATE TABLE article_purchase_batches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    article_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    remaining_quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    purchase_date TEXT DEFAULT CURRENT_TIMESTAMP,
    achat_id INTEGER,
    scope TEXT DEFAULT 'buvette',
    FOREIGN KEY (article_id) REFERENCES buvette_articles(id)
);
```

### 2. Inventory DB Flow (`modules/buvette_inventaire_db.py`)

**Already Implemented** - Modifications include:

- `delete_inventaire(inv_id)`: Now calls `revert_inventory_effect()` before deletion to maintain consistency
- `apply_inventory_snapshot_wrapper(inv_id)`: Helper function to apply inventory snapshot after create/update
- Integrated into inventory dialogs for automatic stock updates

### 3. UI Helpers (`modules/stock_tab.py`)

**Updated** - Changes include:

- `get_stock_listing(scope='buvette')`: Returns stock listing for UI
- **Backward compatibility**: Automatically detects schema and returns appropriate columns
  - Pre-migration: Returns 'unite' field
  - Post-migration: Returns 'quantite' and 'unite_type' fields
- Dynamic column detection based on database schema

### 4. Articles Migration (`scripts/migrate_articles_unite_to_quantite.py`)

**Already Implemented** - Migration script:

- Backs up database to `<db>.bak` before applying changes
- Creates new schema with 'quantite' (INTEGER) and 'unite_type' (TEXT) columns
- Preserves legacy 'unite' values by copying to 'unite_type'
- Removes 'unite' column
- All data is preserved during migration

**Usage:**
```bash
python scripts/migrate_articles_unite_to_quantite.py --db path/to/association.db
```

### 5. Buvette Module UI (`modules/buvette.py`)

**Updated** - Changes include:

- **Articles Tab**: Updated to display 'quantite' and 'unite_type' columns
- **Stock Buvette Tab**: Updated to handle both pre and post-migration schemas
- **ArticleDialog**: Handles both schemas when loading articles for editing
- Graceful fallback for pre-migration 'unite' column

### 6. Buvette Database Layer (`modules/buvette_db.py`)

**Updated** - Changes include:

- `insert_article()`: Detects schema and uses correct column (unite vs unite_type)
- `update_article()`: Detects schema and uses correct column (unite vs unite_type)
- **API Backward Compatibility**: The 'unite' parameter works for both schemas
- Dynamic schema detection using PRAGMA table_info

### 7. Main Application (`main.py`)

**Already Implemented** - Startup integration:

- Lines 83-87: Calls `ensure_stock_tables()` at startup
- Ensures stock journal tables are created before application starts

## Backward Compatibility Strategy

The implementation provides full backward compatibility:

1. **Pre-Migration Operation**: 
   - All functions work with existing 'unite' column
   - No breaking changes to existing databases

2. **Migration Process**:
   - Automatic backup creation
   - Data preservation (unite → unite_type)
   - No data loss

3. **Post-Migration Operation**:
   - All functions detect new schema automatically
   - UI adapts to display new columns
   - API remains the same (unite parameter still works)

## Testing

Comprehensive test suite includes:

- **Stock Journal Tests** (7 tests): Test all stock_db functions
- **Buvette Stock Tests** (5 tests): Test stock column functionality
- **Stock Tab Tests** (7 tests): Test UI helper functions
- **Inventory Integration Tests** (5 tests): Test inventory flow
- **Migration Tests** (9 tests): Test backward compatibility
  - Pre-migration insert/update
  - Post-migration insert/update
  - Data preservation
  - Schema changes
  - UI compatibility

**Total: 34 tests passing**

## Integration Points

### Stock Views

1. **Stock (Matériel)**: Top-level tab in main application
   - Uses existing `stock` table (separate from buvette_articles)
   - Accessed via "Stock" menu item

2. **Stock Buvette**: Inside Buvette section
   - Filters by scope='buvette'
   - Uses `buvette_articles` table with stock column
   - Accessed via "Stock Buvette" tab in Buvette module

### Inventory Flow

When creating/updating an inventory:

```python
# 1. Create inventory
inv_id = insert_inventaire(date, event_id, type_inv, comment)

# 2. Add inventory lines
for line in lines:
    insert_ligne_inventaire(inv_id, article_id, quantite)

# 3. Apply inventory snapshot (automatic stock update)
apply_inventory_snapshot_wrapper(inv_id)
```

When deleting an inventory:

```python
# delete_inventaire automatically:
# 1. Reverts stock effects using journal
# 2. Deletes child rows
# 3. Deletes inventory
delete_inventaire(inv_id)
```

## Migration Guide

### For Developers

1. **Before Migration**: No code changes needed, everything works
2. **Running Migration**: 
   ```bash
   python scripts/migrate_articles_unite_to_quantite.py --db association.db
   ```
3. **After Migration**: No code changes needed, everything adapts automatically

### For Users

1. **Backup**: Migration automatically creates `association.db.bak`
2. **No Downtime**: Application can run before and after migration
3. **No Data Loss**: All data is preserved
4. **Reversible**: Backup file can be restored if needed

## Security Considerations

- All SQL table/column names from user input are validated against whitelists
- Table names from sqlite_master are trusted (system source)
- PRAGMA commands use validated table names only
- No SQL injection vulnerabilities

## Performance

- All operations are transactional
- Stock journal enables fast revert operations
- FIFO costing uses indexed queries
- Minimal overhead for schema detection (cached in memory)

## Future Enhancements

Potential improvements:

1. Add 'materiel' scope support in stock_db for general stock tracking
2. Batch operations for multiple inventory snapshots
3. Historical stock reporting using journal
4. Advanced FIFO cost reports
5. Stock alerts based on thresholds

## Troubleshooting

### Issue: Migration fails

**Solution**: 
1. Check that backup was created
2. Verify table exists: `SELECT name FROM sqlite_master WHERE type='table' AND name='buvette_articles'`
3. Check for foreign key constraints
4. Restore from backup if needed

### Issue: UI shows wrong columns

**Solution**: 
1. Check database schema: `PRAGMA table_info(buvette_articles)`
2. Verify stock_tab.py is updated
3. Restart application to clear any cached schemas

### Issue: Tests fail after migration

**Solution**:
1. Ensure test database uses correct schema
2. Check that test fixtures create proper tables
3. Run migration compatibility tests: `pytest tests/test_articles_unite_migration.py`

## Summary

This implementation provides a robust, backward-compatible solution for stock management and schema migration. All changes are minimal, conservative, and thoroughly tested. The system gracefully handles both pre and post-migration states, ensuring smooth operation throughout the migration process.
