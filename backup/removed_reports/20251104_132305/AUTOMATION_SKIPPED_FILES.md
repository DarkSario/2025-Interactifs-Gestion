# Automation Skipped Files - Buvette Module Fixes

This document lists files that were skipped during automated buvette module fixes
due to complexity, ambiguity, or risk of breaking existing functionality.

## Overview

During the invasive audit, several buvette-related improvements were identified but
not automatically applied. These fixes require manual review and testing.

## Categories of Skipped Fixes

### 1. Complex UI Modifications

**Files Skipped**:
- `modules/buvette_dialogs.py`
- `modules/buvette_inventaire_dialogs.py`
- `modules/buvette_mouvements_dialogs.py`
- `dashboard/dashboard.py`

**Reason**: 
UI dialog modifications require careful testing to ensure:
- Field layouts remain visually correct
- Validation logic works as expected
- User workflows are not disrupted
- Tkinter widget bindings function properly

**Recommended Action**:
- Manual review of each dialog class
- Add explicit fields for price/quantity where needed
- Test with various screen sizes and user scenarios

### 2. Ambiguous Row.get() Conversions

**Files with Ambiguous Patterns**:

#### `modules/buvette.py` (12 instances)
Lines with `.get()` usage that may need conversion:
- Line 436: `item.get("unite_type", item.get("unite", ""))`
- Line 437: `item.get("quantite", "")`
- Line 441-449: Multiple `.get()` calls in tree population
- Line 503: Nested `.get()` with fallback
- Line 519: Optional purchase_price check

**Risk**: These patterns suggest the code already expects dict-like objects.
Blindly converting could introduce redundant conversions or break existing logic.

**Recommended Action**:
- Trace the source of `item` and `article` variables
- Verify if they're already dicts from repository methods
- If not, add row_to_dict() at the source (repository return)

#### `modules/members.py` (5 instances)
Lines 67-69: Multiple `.get()` calls with default values

**Risk**: Member records may already be dicts from the database layer.

**Recommended Action**:
- Check if `modules/members_db.py` returns dicts or Row objects
- Add row_to_dict() in the repository if needed

#### `modules/stock_db.py` (Multiple instances)
**Risk**: Stock database module has complex inventory tracking logic.

**Recommended Action**:
- Review each function's return type
- Normalize all returns to dicts using rows_to_dicts()
- Update function docstrings to document return types

### 3. Stock Recomputation Logic

**Files Requiring Manual Implementation**:
- `modules/buvette_db.py` - needs `recompute_stock_for_article()` function
- `modules/buvette_inventaire_db.py` - needs to call recompute on delete

**Current Status**: Partially implemented in previous work

**Remaining Work**:
1. Verify `recompute_stock_for_article()` exists and works correctly
2. Add call to recompute after inventory deletion
3. Add call to recompute after inventory addition
4. Ensure stock updates are transactional

**Risk**: 
- Stock calculation errors could lead to inventory discrepancies
- Must be tested thoroughly with various scenarios

### 4. Purchase Price Updates

**Files Requiring Updates**:
- `modules/buvette_inventaire_db.py` - update purchase_price on inventory add
- `modules/buvette_db.py` - update purchase_price on achat

**Current Status**: Some logic exists but needs verification

**Remaining Work**:
1. Ensure purchase_price is updated when prix_unitaire is provided
2. Add validation for negative or zero prices
3. Log price changes for audit trail
4. Test edge cases (NULL prices, zero quantities, etc.)

**Risk**:
- Incorrect price updates could affect financial reports
- Must preserve historical price data integrity

### 5. UI Refresh Calls

**Files Needing Explicit refresh_*() Calls**:
- `modules/buvette.py` - after DB modifications
- `modules/buvette_inventaire_dialogs.py` - after inventory operations
- `dashboard/dashboard.py` - after buvette state changes

**Current Status**: Some refresh calls exist

**Remaining Work**:
1. Audit all DB modification points
2. Add explicit refresh calls after:
   - Article creation/update/deletion
   - Inventory addition/deletion
   - Stock movements
   - Price changes
3. Ensure refreshes don't cause performance issues

**Risk**:
- Missing refreshes lead to stale UI data
- Excessive refreshes cause UI sluggishness

## Files Successfully Automated

The following areas were successfully handled:

### ✓ Database Utilities
- `src/db/row_utils.py` - Already exists and works correctly
- `src/db/repository.py` - Already normalizes to dicts
- `src/db/connection.py` - Proper connection management

### ✓ Exports Package
- `exports/exports.py` - Restored and working
- `exports/export_bilan_argumente.py` - Restored and working
- `modules/exports.py` - Shim layer added successfully

## Summary Statistics

| Category | Files Skipped | Reason |
|----------|---------------|--------|
| UI Dialogs | 4 | Complex UI modifications require manual testing |
| Row.get() Conversions | 8 | Ambiguous patterns, risk of breaking existing code |
| Stock Logic | 2 | Critical business logic requires careful review |
| Price Updates | 2 | Financial integrity concerns |
| UI Refreshes | 3 | Requires comprehensive workflow testing |
| **Total** | **19** | **Various complexity and risk factors** |

## Prioritization Recommendations

### High Priority (Critical for Correctness)
1. Stock recomputation logic verification
2. Purchase price update validation
3. Database return normalization in buvette_db.py

### Medium Priority (User Experience)
1. UI refresh calls after DB operations
2. Dialog field additions for price/quantity
3. Row.get() conversions in display code

### Low Priority (Code Quality)
1. Refactoring complex nested .get() calls
2. Adding type hints to function signatures
3. Improving error messages in dialogs

## Testing Requirements

Before marking any skipped file as "done", ensure:

1. **Unit Tests Pass**: All existing tests continue to work
2. **Integration Tests**: End-to-end workflows function correctly
3. **Manual Testing**: UI interactions are smooth and intuitive
4. **Edge Cases**: Handle NULL values, empty strings, zero quantities
5. **Error Handling**: Graceful degradation on errors

## Action Items for Manual Review

See `reports/TODOs.md` for specific TODO items that need to be addressed.

Key items:
- [ ] Review and apply row.get() conversions in modules/buvette.py
- [ ] Verify recompute_stock_for_article implementation
- [ ] Add explicit refresh calls after all DB modifications
- [ ] Test purchase price update logic thoroughly
- [ ] Update UI dialogs to expose price fields where needed

## Notes

This invasive audit provides a comprehensive analysis but stops short of making
automatic changes where manual review is safer. The goal is reversibility and
correctness over speed.

All skipped fixes are documented in this file and in TODOs.md for future action.

---

# Exports Centralization - Skipped Files

This section lists files that were intentionally skipped during the automated exports import centralization process.

## Intentionally Skipped Files for Exports Centralization

### Package Definition Files

- `exports/__init__.py` - This IS the exports package itself. It defines the package's public API and should not have its internal imports modified.

### Shim/Compatibility Layer Files

- `modules/exports.py` - This is a compatibility shim layer that re-exports from the exports package. It provides backward compatibility and defines additional UI components (like ExportsWindow) that are not part of the core exports package. Its internal structure should be preserved.

### Imports That Should NOT Be Changed

The following imports from `modules.exports` should remain unchanged because these items are defined in `modules/exports.py` and not in the core `exports` package:

- `ExportsWindow` - UI class for exports management
- `export_bilan_evenement` - Event-specific export function
- `export_depenses_global` - Global expenses export
- `export_subventions_global` - Global subsidies export  
- `export_tous_bilans_evenements` - Bulk event export

### Test Files

All files in the `tests/` directory were excluded as per project policy. Test files may contain intentional import patterns for testing purposes.

### Migration Scripts

All files matching patterns:
- `scripts/migration*`
- `scripts/migrate_*`

These scripts are one-time migration utilities and should not be modified.

## Files Successfully Modified by Automation

The exports centralization automation successfully modified:

1. `modules/cloture_exercice.py` - Import from `exports.exports` centralized to `exports`
2. `modules/event_modules.py` - Imports from `exports.exports` centralized to `exports` and sys.path hacks removed

## Rationale for Skipping

The automation script is designed to be conservative and only modify application code files where:
1. The import pattern is unambiguous
2. The change is safe and will not break functionality
3. The file is not a special system file (package definitions, shims, tests, migrations)

All other files should be manually reviewed if import centralization is desired.
