# TODO Items Report

This report lists all TODO and FIXME comments in the codebase,
including those added by automated changes.

Generated: /home/runner/work/2025-Interactifs-Gestion/2025-Interactifs-Gestion

## Summary

Total TODO/FIXME items: 62

## Items by File

### modules/buvette.py

- Line 16: TODO (audit/fixes-buvette):
- Line 18: - Review reports/TODOs.md for additional audit findings
- Line 288: # TODO (audit/fixes-buvette): Consider batch refresh or async mechanism
- Line 291: # See reports/TODOs.md for UI refresh strategy review

### modules/buvette_bilan_db.py

- Line 9: TODO (audit/fixes-buvette):
- Line 11: - Review reports/TODOs.md for additional audit findings

### modules/buvette_db.py

- Line 22: TODO (audit/fixes-buvette):
- Line 24: - Review reports/TODOs.md for additional audit findings
- Line 229: TODO (audit/fixes-buvette): Review price update strategy.
- Line 233: See reports/TODOs.md for pricing strategy review.
- Line 271: TODO (audit/fixes-buvette): Review if price should update on achat modification.
- Line 275: See reports/TODOs.md for pricing strategy review.

### modules/buvette_inventaire_db.py

- Line 13: TODO (audit/fixes-buvette):
- Line 15: - Review reports/TODOs.md for additional audit findings
- Line 132: TODO (audit/fixes-buvette): Review deletion workflow order.
- Line 136: See reports/TODOs.md for process review.
- Line 268: TODO (audit/fixes-buvette): Verify stock recalculation after line deletion.
- Line 269: See reports/TODOs.md for implementation review.

### modules/buvette_mouvements_db.py

- Line 9: TODO (audit/fixes-buvette):
- Line 11: - Review reports/TODOs.md for additional changes
- Line 29: TODO (audit/fixes-buvette): Added aliases for UI compatibility
- Line 58: TODO (audit/fixes-buvette): Added aliases for UI compatibility

### modules/cloture_exercice.py

- Line 8: from exports import (  # TODO: automated centralization change — see reports/TODOs.md

### modules/event_modules.py

- Line 550: from exports import export_dataframe_to_pdf  # TODO: automated centralization change — see reports/TODOs.md
- Line 583: from exports import export_dataframe_to_excel  # TODO: automated centralization change — see reports/TODOs.md

### modules/stock_db.py

- Line 478: TODO (audit/fixes-buvette):
- Line 482: See reports/TODOs.md for implementation review.

### scripts/audit_db_usage.py

- Line 10: - Generate reports in reports/SQL_ACCESS_MAP.md and reports/TODOs.md
- Line 253: """Generate TODOs.md report with action items."""
- Line 255: report.append("# Database Access TODOs\n")
- Line 325: print("\nGenerating TODOs.md...")
- Line 327: todos_path = reports_dir / 'TODOs.md'
- Line 343: print("\n⚠️  CRITICAL issues found! See TODOs.md for action items.")

### scripts/generate_audit_reports.py

- Line 8: - TODOs.md: List of all TODO comments from automated changes
- Line 179: """Scan for TODO comments in the codebase."""
- Line 192: if 'TODO' in line or 'FIXME' in line:
- Line 203: """Generate TODOs.md report."""
- Line 207: lines.append("# TODO Items Report")
- Line 209: lines.append("This report lists all TODO and FIXME comments in the codebase,")
- Line 217: lines.append(f"Total TODO/FIXME items: {len(todos)}")
- Line 307: generate_todos_report(root_dir, reports_dir / 'TODOs.md')

### scripts/project_audit.py

- Line 10: - TODO/FIXME/XXX comments
- Line 106: """Analyze Python files for imports, TODOs, and other issues."""
- Line 126: # Search for TODO/FIXME/XXX comments
- Line 188: """Find TODO/FIXME/XXX comments in the content."""
- Line 190: patterns = [r'#\s*(TODO|FIXME|XXX)', r'"""\s*(TODO|FIXME|XXX)', r"'''\s*(TODO|FIXME|XXX)"]
- Line 334: report.append(f"- **TODO/FIXME/XXX comments**: {len(self.todos)}")
- Line 485: # TODOs
- Line 487: report.append("## 📝 TODO/FIXME/XXX Comments")
- Line 489: report.append(f"Found {len(self.todos)} TODO/FIXME/XXX comment(s):")
- Line 492: # Show first 20 TODOs
- Line 586: report.append("2. **Address TODO/FIXME comments**")
- Line 587: report.append("   - Create issues for important TODOs")
- Line 588: report.append("   - Remove or complete outdated TODOs")
- Line 655: print(f"TODO/FIXME/XXX: {len(self.todos)}")

### scripts/replace_row_get.py

- Line 143: # TODO: Implement automatic fixes using RowGetTransformer

### scripts/safe_replace_exports.py

- Line 11: 3. Adds TODO comments for automated changes
- Line 40: r'from exports import \1  # TODO: automated centralization change — see reports/TODOs.md'
- Line 45: r'from exports import \1  # TODO: automated centralization change — see reports/TODOs.md'
- Line 50: r'from exports import \1  # TODO: automated centralization change — see reports/TODOs.md'
- Line 129: # Check if line already has a TODO comment
- Line 130: if '# TODO: automated centralization change' not in line:
