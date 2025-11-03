# Replace sqlite3.connect Report

**Date:** 2025-11-03  
**Branch:** audit/fixes-buvette  
**Script:** scripts/replace_sqlite_connect.py

## Summary

The replace_sqlite_connect.py script was run to identify files using direct sqlite3.connect() calls that should be replaced with get_connection() for consistency.

## Skip Logic

The script has been updated to skip:
- Test files (tests/)
- Migration scripts (migration*.py, migrate_*.py)
- Database diagnostics and utilities (db_diagnostics.py, enable_wal.py, etc.)
- Core infrastructure files that define get_connection (db/db.py, modules/db_api.py, src/db/compat.py, src/db/connection.py)

## Results

**Files that would be modified:** 0

All files that use sqlite3.connect() are either:
1. Core infrastructure that DEFINES get_connection (needs sqlite3.connect internally)
2. Migration scripts that must remain raw for safety
3. Test files that are intentionally using direct connections

## Conclusion

✅ No changes needed - all sqlite3.connect() usage is appropriate and should not be replaced.

The buvette modules already use get_connection() consistently, which was one of the main goals of this audit.

## Files Analyzed

Files that use sqlite3.connect() (correctly skipped):
- db/db.py - Defines get_connection
- modules/db_api.py - Defines get_connection  
- src/db/compat.py - Defines get_connection
- src/db/connection.py - Core connection infrastructure
- scripts/migrate_articles_unite_to_quantite.py - Migration script (must remain raw)
- scripts/migrate_add_purchase_price.py - Migration script (must remain raw)
- scripts/migration.py - Migration script (must remain raw)
- scripts/update_db_structure.py - Database utility (must remain raw)
- scripts/update_db_structure_old.py - Database utility (must remain raw)
- scripts/db_diagnostics.py - Diagnostic utility (must remain raw)
- scripts/enable_wal.py - Database utility (must remain raw)
- scripts/create_compat_views.py - Database utility (must remain raw)
- tests/* - Test files (intentionally use direct connections)

## Verification

To verify buvette modules use get_connection:
```bash
grep -n "from db.db import get_connection" modules/buvette*.py
```

Result: All buvette modules correctly use get_connection() ✅
