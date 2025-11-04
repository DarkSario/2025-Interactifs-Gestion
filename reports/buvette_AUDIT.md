# Buvette Module Audit

Comprehensive audit of the buvette (snack bar) module.

Generated: /home/runner/work/2025-Interactifs-Gestion/2025-Interactifs-Gestion

## Summary

- Total buvette-related files: 17

## Files

- `modules/buvette.py` (45899 bytes)
- `modules/buvette_bilan_db.py` (3525 bytes)
- `modules/buvette_bilan_dialogs.py` (4091 bytes)
- `modules/buvette_db.py` (19721 bytes)
- `modules/buvette_dialogs.py` (15617 bytes)
- `modules/buvette_inventaire_db.py` (13825 bytes)
- `modules/buvette_inventaire_dialogs.py` (21532 bytes)
- `modules/buvette_mouvements_db.py` (4631 bytes)
- `modules/buvette_mouvements_dialogs.py` (4000 bytes)
- `scripts/auto_fix_buvette_rows.py` (9016 bytes)
- `scripts/check_buvette.py` (14546 bytes)
- `tests/test_buvette_audit.py` (13795 bytes)
- `tests/test_buvette_inventaire.py` (9057 bytes)
- `tests/test_buvette_purchase_price.py` (7034 bytes)
- `tests/test_buvette_repository.py` (10422 bytes)
- `tests/test_buvette_stock.py` (5928 bytes)
- `tests/test_stock_buvette_tab.py` (7601 bytes)

## Known Issues

### Missing Columns
- `buvette_inventaire_lignes.commentaire` - Added via migration 0001

## Recommendations

1. Review all buvette database queries for proper error handling
2. Ensure row_to_dict() is used for all database row access
3. Add comprehensive tests for buvette inventory operations
