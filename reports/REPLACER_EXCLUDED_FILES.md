# Excluded Files from AST Replacers

This document lists files that were intentionally excluded from the AST replacement scripts
(`replace_row_get.py` and `replace_sqlite_connect.py`) during the invasive audit.

## Exclusion Criteria

Files were excluded based on the following criteria:
1. Located in `tests/` directory - test files should not be auto-modified
2. Matching pattern `scripts/migration*.py` - migration scripts are sensitive
3. Located in automatically-skipped directories (`.git`, `__pycache__`, `venv`, etc.)

## Excluded Directories (Auto-skipped)

The following directories are automatically skipped by the replacer scripts:
- `.git/`
- `__pycache__/`
- `venv/`
- `env/`
- `.pytest_cache/`
- `node_modules/`
- `dist/`
- `build/`
- `reports/`

## Explicitly Excluded Files

### Test Files (tests/)

All files in the `tests/` directory were excluded from automatic replacement:

- `tests/test_analyze_modules.py`
- `tests/test_articles_unite_migration.py`
- `tests/test_buvette_audit.py`
- `tests/test_buvette_inventaire.py`
- `tests/test_buvette_purchase_price.py`
- `tests/test_buvette_repository.py`
- `tests/test_buvette_stock.py`
- `tests/test_connection.py`
- `tests/test_database_migration.py`
- `tests/test_db_api_retry.py`
- `tests/test_db_locking.py`
- `tests/test_db_row_utils.py`
- `tests/test_delete_inventaire.py`
- `tests/test_example.py`
- `tests/test_inventory_integration.py`
- `tests/test_inventory_lines_loader.py`
- `tests/test_inventory_service.py`
- `tests/test_repository.py`
- `tests/test_row_to_dict_conversion.py`
- `tests/test_smart_migration.py`
- `tests/test_src_row_utils.py`
- `tests/test_startup_schema_check.py`
- `tests/test_stock_buvette_tab.py`
- `tests/test_stock_journal.py`
- `tests/test_utils.py`

### Migration Scripts (scripts/migration*.py)

Migration scripts were excluded due to their sensitive nature:

- `scripts/migrate_add_purchase_price.py`
- `scripts/migrate_articles_unite_to_quantite.py`
- `scripts/migration.py`

## Rationale

### Why Exclude Tests?

Test files are excluded because:
1. They often intentionally test edge cases and error conditions
2. They may use mock objects that don't match runtime behavior
3. Automatic modifications could break test assertions
4. Test files should be manually reviewed if changes are needed

### Why Exclude Migration Scripts?

Migration scripts are excluded because:
1. They are one-time operations that may already have been executed
2. Modifying them could create inconsistencies in migration history
3. They often require careful manual review of DB state changes
4. They may contain deliberate patterns that should not be modified

## Files with Issues Detected

### replace_row_get.py Findings

The following files had `.get()` usage on potential sqlite3.Row objects detected:

**Total**: 68 issues found in 16 files

Key files with issues:
- `modules/buvette.py` (12 issues)
- `modules/members.py` (5 issues)
- `modules/stock_db.py` (multiple issues)
- `modules/buvette_inventaire_dialogs.py` (5 issues)
- `modules/depots_retraits_banque.py` (4 issues)
- Others (see SQL_ACCESS_MAP.md for full details)

### replace_sqlite_connect.py Findings

**Total**: 0 files required replacement

The `replace_sqlite_connect.py` script found no instances requiring replacement,
indicating that the codebase already uses the proper connection patterns.

## Recommendations

1. **Manual Review Required**: Files in the excluded list should be manually reviewed
   if they need updates related to row.get() patterns

2. **Test Maintenance**: Test files should be updated separately if the application
   API changes significantly

3. **Migration Audits**: Migration scripts should remain unchanged unless there's
   a critical bug that requires a fix

## Next Steps

For files that were NOT excluded but have issues:
1. Review the SQL_ACCESS_MAP.md report
2. Apply fixes manually or verify they're already handled
3. Update TODOs.md with any remaining action items
