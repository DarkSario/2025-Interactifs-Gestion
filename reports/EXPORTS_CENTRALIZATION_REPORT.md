# Exports Centralization Report

This report shows all files that were analyzed for exports import centralization.

## Summary

- Total files analyzed: 110
- Files with changes: 2
- Total import changes: 3
- Total sys.path hacks removed: 2
- Files with errors: 0

## Files Modified

### /home/runner/work/2025-Interactifs-Gestion/2025-Interactifs-Gestion/modules/cloture_exercice.py

**Import Changes:**

Line 8:
- Before: `from exports.exports import (`
- After: `from exports import (  # TODO: automated centralization change — see reports/TODOs.md`

### /home/runner/work/2025-Interactifs-Gestion/2025-Interactifs-Gestion/modules/event_modules.py

**Import Changes:**

Line 554:
- Before: `from exports.exports import export_dataframe_to_pdf`
- After: `from exports import export_dataframe_to_pdf  # TODO: automated centralization change — see reports/TODOs.md`

Line 591:
- Before: `from exports.exports import export_dataframe_to_excel`
- After: `from exports import export_dataframe_to_excel  # TODO: automated centralization change — see reports/TODOs.md`

**Sys.path Hacks Removed:**

Lines 550-554:
```python
            import sys, os
            parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            if parent_dir not in sys.path:
                sys.path.append(parent_dir)
```

Lines 587-591:
```python
            import sys, os
            parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            if parent_dir not in sys.path:
                sys.path.append(parent_dir)
```

