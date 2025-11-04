# Database Migrations

This directory contains SQL migration scripts for the database schema.

## Migration Naming Convention

Migrations follow the pattern: `NNNN_description.sql`

Where:
- `NNNN` is a 4-digit sequential number (0001, 0002, etc.)
- `description` is a short snake_case description

## Running Migrations

Use the migration runner script:

```bash
# Dry-run (check what would be applied)
python scripts/apply_migrations.py --dry-run

# Apply migrations
python scripts/apply_migrations.py

# Check status
python scripts/apply_migrations.py --status
```

## Migration Guidelines

1. **Idempotent**: Migrations should be safe to run multiple times
2. **Additive Only**: Never drop columns or tables (mark as deprecated instead)
3. **Test First**: Always test migrations on a backup database
4. **Document**: Include clear comments explaining the change

## Migration Files

- `0001_add_commentaire_buvette_inventaire_lignes.sql` - Adds missing commentaire column to buvette inventory lines
