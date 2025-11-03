# Column Removal Candidates for Manual Review

**Generated:** 2025-11-03  
**Purpose:** List columns that may be candidates for removal or migration  
**Status:** All candidates require manual review before any action

---

## Overview

This document lists database columns that are candidates for removal, renaming, or migration. **NO AUTOMATED CHANGES SHOULD BE APPLIED** to these columns without careful manual review, as they may affect existing functionality or data integrity.

---

## Analysis Summary

Based on the comprehensive audit of the buvette module and database access patterns:

### ✅ NO REMOVAL CANDIDATES FOUND

After analyzing the codebase, **no columns were identified as safe candidates for removal** in the buvette tables:

- **buvette_articles**: All columns (id, name, categorie, stock, prix_vente, contenance, unite, commentaire, purchase_price) are actively used
- **buvette_mouvements**: All columns (id, article_id, date_mouvement, type_mouvement, quantite, motif, event_id) are actively used  
- **buvette_inventaires**: All columns (id, date_inventaire, event_id, type_inventaire, commentaire) are actively used
- **buvette_inventaire_lignes**: All columns (id, inventaire_id, article_id, quantite, commentaire) are actively used
- **buvette_achats**: All columns are used for financial calculations
- **buvette_recettes**: All columns are used for financial reporting

---

## Migration History (Reference)

### ✅ COMPLETED MIGRATIONS

These migrations have already been successfully completed and do not require further action:

1. **Column Name Standardization (buvette_mouvements)**
   - `date` → `date_mouvement` ✓ COMPLETED
   - `type` → `type_mouvement` ✓ COMPLETED  
   - `commentaire` → `motif` ✓ COMPLETED
   - Status: Schema updated, queries use proper aliases for UI compatibility

2. **Stock Column Addition (buvette_articles)**
   - Added `stock` column with non-destructive migration
   - Status: ✓ COMPLETED and working

3. **Purchase Price Addition (buvette_articles)**
   - Added `purchase_price` column for cost tracking
   - Status: ✓ COMPLETED and integrated

---

## Future Considerations (Non-Urgent)

### Schema Design Improvements (Low Priority)

These are architectural improvements that could be considered in future major versions, but should NOT be implemented now:

1. **Event ID Consistency**
   - Some tables use `event_id` with different FK constraints
   - Consider: Standardize ON DELETE behavior across all event FKs
   - Risk: Low (current implementation is working)
   - Priority: LOW - only for future major version

2. **Article Unite Field**
   - Currently uses TEXT field for unit types
   - Consider: Enum or separate units table for consistency
   - Risk: Low (current TEXT approach is flexible)
   - Priority: LOW - only if strict validation needed

3. **Inventory Type Validation**
   - Currently uses TEXT for type_inventaire
   - Values: 'avant', 'apres', 'hors_evenement'
   - Consider: CHECK constraint or enum
   - Risk: Very Low (validation exists in application layer)
   - Priority: LOW - current approach is working fine

---

## Recommendations

### ✅ DO:
- Keep all existing columns in buvette tables
- Maintain current schema structure
- Continue using SELECT aliases for UI compatibility
- Use non-destructive migrations for future changes

### ❌ DO NOT:
- Remove any columns from buvette tables (all are in use)
- Apply automated structural changes without testing
- Modify column types without migration script
- Drop or rename columns without thorough impact analysis

---

## Review Process for Future Column Changes

If a column needs to be removed in the future, follow this process:

1. **Analysis Phase**
   - Run `scripts/audit_db_usage.py` to check usage
   - Search codebase for column references
   - Check all SELECT, INSERT, UPDATE statements
   - Verify no UI components depend on the column

2. **Planning Phase**
   - Document all code locations that use the column
   - Create migration script with rollback capability
   - Plan database backup strategy
   - Identify testing requirements

3. **Testing Phase**
   - Test migration on copy of production database
   - Verify all features work without the column
   - Run full test suite
   - Perform manual UI testing

4. **Deployment Phase**
   - Backup production database
   - Run migration during maintenance window
   - Monitor for errors
   - Have rollback plan ready

---

## Conclusion

**No structural changes are recommended at this time.** All columns in the buvette module are actively used and serve important purposes. The module is well-designed and functioning correctly.

Any future column changes should follow the review process above and should not be automated.

---

**Last Updated:** 2025-11-03  
**Next Review:** As needed when schema changes are proposed  
**Document Owner:** Database Architecture Team
