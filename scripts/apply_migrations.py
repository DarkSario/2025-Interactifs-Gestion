#!/usr/bin/env python3
"""
Database Migration Runner

This script applies SQL migration files in order, tracking which migrations
have been applied to avoid re-running them.

Usage:
    python scripts/apply_migrations.py               # Apply pending migrations
    python scripts/apply_migrations.py --dry-run     # Show what would be applied
    python scripts/apply_migrations.py --status      # Show migration status
    python scripts/apply_migrations.py --force FILE  # Force re-run a migration

Features:
    - Idempotent: Tracks applied migrations
    - Transaction-safe: Each migration runs in a transaction
    - Automatic backup before applying
    - Sequential execution by filename
"""

import sqlite3
import argparse
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Tuple
import shutil


MIGRATIONS_DIR = Path("migrations")
MIGRATIONS_TABLE = "_migrations"


def get_db_path() -> Path:
    """Get the database file path."""
    candidates = [
        Path("db/association.db"),
        Path("association.db"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError("Database file not found")


def backup_database(db_path: Path) -> Path:
    """
    Create a backup of the database.
    
    Returns:
        Path to backup file
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = db_path.parent / f"{db_path.stem}.bak.{timestamp}{db_path.suffix}"
    shutil.copy2(db_path, backup_path)
    return backup_path


def init_migrations_table(conn: sqlite3.Connection):
    """Create migrations tracking table if it doesn't exist."""
    conn.execute(f"""
        CREATE TABLE IF NOT EXISTS {MIGRATIONS_TABLE} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL UNIQUE,
            applied_at TEXT NOT NULL,
            checksum TEXT
        )
    """)
    conn.commit()


def get_applied_migrations(conn: sqlite3.Connection) -> set:
    """Get set of already-applied migration filenames."""
    cursor = conn.cursor()
    cursor.execute(f"SELECT filename FROM {MIGRATIONS_TABLE}")
    return {row[0] for row in cursor.fetchall()}


def get_migration_files() -> List[Path]:
    """Get all migration SQL files, sorted by filename."""
    if not MIGRATIONS_DIR.exists():
        return []
    
    migrations = sorted(
        MIGRATIONS_DIR.glob("*.sql"),
        key=lambda p: p.name
    )
    return migrations


def apply_migration(conn: sqlite3.Connection, migration_file: Path, dry_run: bool = False) -> bool:
    """
    Apply a single migration file.
    
    Returns:
        True if successful, False otherwise
    """
    print(f"\nApplying: {migration_file.name}")
    
    try:
        sql = migration_file.read_text()
        
        if dry_run:
            print(f"  [DRY-RUN] Would execute:")
            print("  " + "\n  ".join(sql.split('\n')[:10]))  # Show first 10 lines
            if len(sql.split('\n')) > 10:
                print("  ...")
            return True
        
        # Execute in transaction
        conn.execute("BEGIN")
        try:
            # Execute the migration SQL
            conn.executescript(sql)
            
            # Record migration as applied
            conn.execute(
                f"INSERT INTO {MIGRATIONS_TABLE} (filename, applied_at) VALUES (?, ?)",
                (migration_file.name, datetime.now().isoformat())
            )
            
            conn.commit()
            print(f"  ✓ Successfully applied: {migration_file.name}")
            return True
            
        except Exception as e:
            conn.rollback()
            print(f"  ✗ Error applying migration: {e}")
            return False
            
    except Exception as e:
        print(f"  ✗ Error reading migration file: {e}")
        return False


def show_status(conn: sqlite3.Connection):
    """Show status of all migrations."""
    migrations = get_migration_files()
    applied = get_applied_migrations(conn)
    
    print("\n" + "=" * 70)
    print("MIGRATION STATUS")
    print("=" * 70)
    print()
    
    if not migrations:
        print("No migration files found in migrations/")
        return
    
    print(f"{'Status':<10} {'Filename':<50} {'Applied At':<20}")
    print("-" * 70)
    
    # Show applied migrations with timestamps
    cursor = conn.cursor()
    cursor.execute(f"SELECT filename, applied_at FROM {MIGRATIONS_TABLE} ORDER BY id")
    applied_details = {row[0]: row[1] for row in cursor.fetchall()}
    
    for migration in migrations:
        if migration.name in applied:
            applied_at = applied_details.get(migration.name, 'Unknown')
            # Shorten timestamp for display
            if 'T' in applied_at:
                applied_at = applied_at.split('T')[0]
            print(f"{'✓ Applied':<10} {migration.name:<50} {applied_at:<20}")
        else:
            print(f"{'Pending':<10} {migration.name:<50} {'-':<20}")
    
    print()
    print(f"Total migrations: {len(migrations)}")
    print(f"Applied: {len(applied)}")
    print(f"Pending: {len(migrations) - len(applied)}")


def main():
    parser = argparse.ArgumentParser(
        description='Apply database migrations'
    )
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be applied without applying')
    parser.add_argument('--status', action='store_true',
                       help='Show migration status')
    parser.add_argument('--force', metavar='FILE',
                       help='Force re-run a specific migration')
    args = parser.parse_args()
    
    try:
        db_path = get_db_path()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1
    
    # Connect to database
    conn = sqlite3.connect(str(db_path))
    
    try:
        # Initialize migrations table
        init_migrations_table(conn)
        
        # Show status if requested
        if args.status:
            show_status(conn)
            return 0
        
        # Get migrations to apply
        all_migrations = get_migration_files()
        applied_migrations = get_applied_migrations(conn)
        
        if args.force:
            # Force re-run a specific migration
            force_file = MIGRATIONS_DIR / args.force
            if not force_file.exists():
                print(f"Error: Migration file not found: {args.force}")
                return 1
            
            print(f"Forcing re-run of: {args.force}")
            
            if not args.dry_run:
                # Remove from applied list
                conn.execute(f"DELETE FROM {MIGRATIONS_TABLE} WHERE filename = ?", (args.force,))
                conn.commit()
                
                # Create backup
                backup_path = backup_database(db_path)
                print(f"Backup created: {backup_path}")
            
            success = apply_migration(conn, force_file, dry_run=args.dry_run)
            return 0 if success else 1
        
        # Normal migration application
        pending_migrations = [
            m for m in all_migrations 
            if m.name not in applied_migrations
        ]
        
        if not pending_migrations:
            print("✓ All migrations are up to date!")
            return 0
        
        # Mode banner
        if args.dry_run:
            print("=" * 70)
            print("DRY-RUN MODE (use without --dry-run to apply)")
            print("=" * 70)
        else:
            print("=" * 70)
            print("APPLYING MIGRATIONS")
            print("=" * 70)
            
            # Create backup before applying
            print(f"\nCreating backup...")
            backup_path = backup_database(db_path)
            print(f"✓ Backup created: {backup_path}")
        
        print(f"\nFound {len(pending_migrations)} pending migration(s):")
        for m in pending_migrations:
            print(f"  - {m.name}")
        
        # Apply migrations
        success_count = 0
        for migration in pending_migrations:
            if apply_migration(conn, migration, dry_run=args.dry_run):
                success_count += 1
            else:
                print(f"\n✗ Migration failed: {migration.name}")
                print("Stopping here to prevent further issues.")
                return 1
        
        # Summary
        print()
        print("=" * 70)
        print("MIGRATION SUMMARY")
        print("=" * 70)
        print(f"Migrations applied: {success_count}/{len(pending_migrations)}")
        
        if args.dry_run:
            print("\nNote: This was a dry-run. Run without --dry-run to apply.")
        else:
            print("\n✓ All migrations applied successfully!")
        
        return 0
        
    finally:
        conn.close()


if __name__ == '__main__':
    sys.exit(main())
