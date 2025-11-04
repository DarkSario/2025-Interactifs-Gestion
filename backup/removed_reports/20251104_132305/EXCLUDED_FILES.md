# Excluded Files Report

This document lists files that were intentionally excluded from automated modifications during the audit and centralization process.

## Purpose

Certain files are excluded from automated transformations to:
1. Preserve test integrity
2. Protect critical infrastructure
3. Avoid circular dependencies
4. Maintain backward compatibility

## Exclusion Categories

### 1. Test Files
**Pattern**: `tests/*`  
**Reason**: Tests should not be modified by automated scripts to maintain their integrity as validation tools.

**Files Excluded**:
- All files in `tests/` directory (27 test files)
- Includes test suites for: buvette, exports, database, inventory, stock, etc.

**Row.get() Detections in Tests** (not modified):
- `tests/test_buvette_audit.py` - 5 occurrences
- `tests/test_buvette_repository.py` - 11 occurrences
- `tests/test_db_api_retry.py` - 2 occurrences

### 2. Migration Scripts
**Pattern**: `scripts/migration*`, `scripts/migrate_*`  
**Reason**: Migration scripts are critical infrastructure and should maintain their original behavior.

**Files Excluded**:
- `scripts/migration.py`
- `scripts/migrate_add_purchase_price.py`
- `scripts/migrate_articles_unite_to_quantite.py`

### 3. Database Infrastructure Files
**Pattern**: Core database connection and compatibility layers  
**Reason**: These files define the database abstraction and connection pooling.

**Files Excluded**:
- `db/db.py` - Main database module
- `src/db/compat.py` - Compatibility layer
- `src/db/connection.py` - Connection management
- `src/db/lock.py` - Database locking utilities

### 4. Diagnostic and Utility Scripts
**Pattern**: `scripts/*_diagnostics.py`, `scripts/enable_wal.py`, etc.  
**Reason**: These scripts interact directly with SQLite internals.

**Files Excluded**:
- `scripts/db_diagnostics.py`
- `scripts/enable_wal.py`
- `scripts/update_db_structure.py`
- `scripts/create_compat_views.py`

### 5. Exports Package Core Files
**Pattern**: `exports/*`  
**Reason**: These are the centralized export functions that other modules import from.

**Files Excluded from Import Replacement**:
- `exports/__init__.py` - Package definition
- `exports/exports.py` - Core export functions
- `exports/export_bilan_argumente.py` - Specialized export functions

### 6. Shim Layer
**Pattern**: `modules/exports.py`  
**Reason**: This is a compatibility shim layer that re-exports from the exports package.

**Files Excluded from Import Replacement**:
- `modules/exports.py` - Intentionally re-exports from exports package

## Statistics

### Files Scanned vs Modified

| Script | Files Scanned | Files Modified | Files Excluded | Exclusion Rate |
|--------|--------------|----------------|----------------|----------------|
| `safe_replace_exports.py` | 113 | 0 | N/A | N/A (already centralized) |
| `replace_sqlite_connect.py` | 113 | 0 (reverted) | 8+ | ~7% |
| `replace_row_get.py` | 113 | 0 (detection only) | 27 | ~24% |

### Row.get() Usage by Category

| Category | Files | Occurrences | Modified |
|----------|-------|-------------|----------|
| Test Files | 3 | 18 | ❌ No (intentional) |
| Production Code | 13 | 50 | ⚠️ Manual review needed |

## Rationale for Each Exclusion Type

### Why Exclude Tests?
- Tests validate the behavior of the system
- Modifying tests could mask bugs
- Tests should be explicit, not automatically transformed
- Test failures are signals, not problems to fix automatically

### Why Exclude Migrations?
- Migration scripts are historical records
- They must remain idempotent and reproducible
- Changing them could break database upgrade paths
- They're often run in production environments

### Why Exclude Core DB Files?
- These define the primitives used by other code
- Circular dependency risk (they might define `get_connection()`)
- Need careful manual review for any changes
- Critical path for all database operations

### Why Exclude Diagnostics?
- These tools use raw SQLite features
- They need direct access to database internals
- They're used for debugging, not production code
- Often intentionally bypass abstractions

## Recommendations

### For Test Files
- Review detected issues manually
- Update tests if they're testing the wrong behavior
- Add new tests for row_to_dict conversions if needed

### For Production Code
- Review the 50 row.get() usages in 13 files
- Add row_to_dict() conversions where appropriate
- Consider wrapping frequently-accessed patterns in helper functions

### For Future Automated Changes
- Always run in dry-run mode first
- Review exclusion lists before applying
- Test thoroughly after any automated modifications
- Keep this document updated with new exclusions

## Files to Review Manually

### High Priority (row.get() in production code)
1. `dashboard/dashboard.py` - 1 occurrence
2. `modules/buvette.py` - 12 occurrences
3. `modules/buvette_bilan_db.py` - 2 occurrences
4. `modules/buvette_inventaire_dialogs.py` - 5 occurrences
5. `modules/depots_retraits_banque.py` - 4 occurrences
6. `modules/event_modules.py` - 1 occurrence
7. `modules/members.py` - 5 occurrences
8. `modules/stock_db.py` - 2 occurrences
9. `modules/stock_inventaire.py` - 1 occurrence

### Medium Priority (utility scripts)
10. New scripts in `scripts/` that use sqlite3.connect directly:
    - `scripts/find_missing_columns.py`
    - `scripts/safe_add_columns.py`
    - `scripts/apply_migrations.py`

## Maintenance Notes

When adding new automated transformation scripts:
1. Define clear exclusion patterns
2. Document the rationale
3. Update this file with new exclusions
4. Test exclusions work correctly
5. Review edge cases

## Version History

- **2025-11-04**: Initial version created during audit/centralize-exports work
- Documented exclusions for: tests, migrations, core DB, diagnostics, exports package

---

For questions about exclusions, see `AUDIT_SUMMARY.md` or contact @DarkSario.
