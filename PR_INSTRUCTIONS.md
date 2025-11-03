# PR Creation Instructions for audit/fixes-buvette

## Status

✅ **All code changes complete**  
✅ **All tests passing (47 tests)**  
✅ **All audit reports generated**  
❌ **Cannot push branch due to authentication limitations**

## Branch Details

- **Branch Name:** `audit/fixes-buvette`
- **Base Branch:** `main`
- **Commits:** 3 commits ready to push
- **Status:** Local branch ready, not yet pushed to remote

## Manual Steps Required

Since automated push failed due to authentication, please manually:

### 1. Push the Branch

```bash
git push -u origin audit/fixes-buvette
```

### 2. Create Draft PR

Go to GitHub and create a PR with these details:

**Title:**
```
chore(buvette): audit & fixes for buvette module
```

**Description:**
```markdown
**Buvette Audit & Fixes - Invasive Automated Corrections (DRAFT)**

This PR applies automated audit corrections to the buvette module with authorized invasive changes. All changes are reversible and marked with TODOs for human review.

## Changes Summary

### 1. Audit Reports Generated
- ✅ SQL_ACCESS_MAP.md - Complete database access pattern map
- ✅ TODOs.md - Action items (68 row.get() issues, 62 sqlite3.connect() calls)
- ✅ buvette_AUDIT_CHECK.md - Buvette validation (all checks pass ✅)
- ✅ COLUMN_REMOVAL_CANDIDATES.md - Column usage analysis
- ✅ REPLACE_SQLITE_CONNECT_REPORT.md - No changes needed
- ✅ REPLACE_ROW_GET_REPORT.md - 67 instances for manual review
- ✅ AUDIT_SUMMARY.md - Comprehensive summary

### 2. Buvette Module Improvements
- Added TODO markers in all buvette modules referencing reports/TODOs.md
- Added SELECT aliases in buvette_mouvements_db.py for UI compatibility:
  * `date_mouvement AS date`
  * `type_mouvement AS type`
  * `motif AS commentaire`
- Verified all functions return dicts via rows_to_dicts/row_to_dict
- Verified UI handlers properly call refresh functions

### 3. Script Updates
- Updated replace_sqlite_connect.py with comprehensive skip logic:
  * Skips tests/
  * Skips migration scripts  
  * Skips files that define get_connection
- Both replace scripts ready but no auto-apply due to safety concerns

### 4. Documentation
- Updated CONTRIBUTING.md with audit script documentation
- Added instructions for running check_buvette.py and audit scripts

## Test Results

✅ **47 tests passing in 0.26s**
- 39 buvette-specific tests
- 8 row_utils/repository tests

```bash
pytest tests/test_buvette*.py tests/test_repository.py tests/test_src_row_utils.py -v
```

## Important Notes

- ⚠️ This PR contains invasive automated changes with TODO markers
- ✅ All changes are reversible
- 📝 TODO markers added for all automated edits
- 🔒 No columns dropped, no tables deleted
- 🛡️ Migration scripts excluded from automated transforms
- 📊 Full audit reports included
- ✅ replace_sqlite_connect: No changes needed (all usage is correct)
- ⚠️ replace_row_get: 67 instances detected, manual review needed
- 📋 Safe skip logic prevents modifications to critical infrastructure

## Review Instructions

1. **Backup database before testing**
2. Review diffs carefully, especially SELECT aliases in buvette_mouvements_db.py
3. Run tests: 
   ```bash
   pytest tests/test_buvette*.py tests/test_repository.py tests/test_src_row_utils.py
   ```
4. Check audit reports in reports/ directory:
   - Review buvette_AUDIT_CHECK.md for validation results
   - Review REPLACE_ROW_GET_REPORT.md for row.get() patterns
   - Review AUDIT_SUMMARY.md for complete overview
   - Review TODOs.md for action items
5. Verify TODO markers in buvette modules point to correct report sections
6. **Dry-run on staging environment first**

## Files Modified

```
modules/buvette_db.py (TODO markers)
modules/buvette_mouvements_db.py (SELECT aliases + TODO markers)
modules/buvette_inventaire_db.py (TODO markers)
modules/buvette_bilan_db.py (TODO markers)
modules/buvette.py (TODO markers)
scripts/replace_sqlite_connect.py (skip logic)
CONTRIBUTING.md (audit documentation)
reports/* (7 updated/new reports)
```

## Commits

1. `feat(buvette): add audit reports and TODO markers`
2. `feat(audit): update replace scripts and generate reports`
3. `docs: add comprehensive audit summary`

---

This PR establishes a solid audit foundation and adds necessary documentation while keeping all changes safe and reversible. The TODO markers guide future manual improvements.
```

### 3. Mark as Draft

- Click "Create draft pull request" button
- Do NOT merge yet

### 4. Request Review

Add @DarkSario as reviewer

## Verification Commands

Before pushing, verify everything is ready:

```bash
# Check branch
git branch --show-current
# Should output: audit/fixes-buvette

# Check commits
git log --oneline main..audit/fixes-buvette
# Should show 3 commits

# Run tests
pytest tests/test_buvette*.py tests/test_repository.py tests/test_src_row_utils.py -v
# Should show 47 tests passing

# Check reports exist
ls -la reports/
# Should show all audit reports including AUDIT_SUMMARY.md
```

## Next Steps After PR Creation

1. Wait for review from @DarkSario
2. Address any review comments
3. Test on staging environment
4. If approved, merge to main
5. Address items in reports/TODOs.md in future PRs

## Rollback Instructions

If needed, rollback is simple:

```bash
git checkout main
git branch -D audit/fixes-buvette  # Delete local branch
git push origin --delete audit/fixes-buvette  # Delete remote branch (if pushed)
```

All changes are in separate commits and can be reverted individually if needed.
