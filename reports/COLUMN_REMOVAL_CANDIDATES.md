# Column Removal Candidates

This report lists database columns that *might* be safe to remove.
⚠️  **CAUTION**: This is for reference only. Never remove columns without thorough testing.

Generated: /home/runner/work/2025-Interactifs-Gestion/2025-Interactifs-Gestion

## Methodology

Columns are considered candidates for removal if:
- They are rarely or never queried in the codebase
- They contain mostly NULL values
- They were added for features that are no longer used

## Candidates

*No automatic detection implemented yet.*

Manual review required. Check:
- Database column usage statistics
- Feature usage analytics
- Historical commit messages

## Recommendation

Instead of removing columns:
1. Mark them as deprecated in documentation
2. Add a migration to remove them in a future version
3. Keep them for backward compatibility if unsure
