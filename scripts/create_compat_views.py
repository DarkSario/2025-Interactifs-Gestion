"""
Create compatibility views for backward compatibility after articles migration.

This script creates a view buvette_articles_compat that exposes the 'unite' column
(mapped from unite_type) so existing SELECT statements referencing 'unite' continue to work
after the migration to quantite/unite_type columns.

Usage:
    python scripts/create_compat_views.py --db path/to/association.db
"""
import sqlite3
import argparse
from pathlib import Path


def create_compat_view(db_path):
    """Create compatibility view for buvette_articles."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        # Check if the table has been migrated (has unite_type column)
        cur = conn.execute("PRAGMA table_info(buvette_articles)")
        cols = [r[1] for r in cur.fetchall()]
        
        if "unite_type" in cols:
            print("Table has been migrated (unite_type column exists)")
            
            # Drop existing view if it exists
            conn.execute("DROP VIEW IF EXISTS buvette_articles_compat")
            
            # Create compatibility view that exposes 'unite' as alias for 'unite_type'
            conn.execute("""
                CREATE VIEW buvette_articles_compat AS
                SELECT 
                    id,
                    name,
                    categorie,
                    quantite,
                    COALESCE(unite_type, '') AS unite,
                    contenance,
                    commentaire,
                    stock,
                    purchase_price
                FROM buvette_articles
            """)
            conn.commit()
            print("Created view: buvette_articles_compat")
            print("  - Exposes 'unite' column (mapped from unite_type)")
            print("  - Use this view in legacy code that expects 'unite' column")
        else:
            print("Table has not been migrated yet (no unite_type column)")
            print("Run migrate_articles_unite_to_quantite.py first")
    except Exception as e:
        print(f"Error creating compatibility view: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(
        description="Create compatibility views for backward compatibility"
    )
    parser.add_argument(
        "--db",
        default="association.db",
        help="Path to sqlite DB"
    )
    args = parser.parse_args()
    db_path = Path(args.db)
    
    if not db_path.exists():
        print(f"DB not found: {db_path}")
        return
    
    create_compat_view(str(db_path))
    print("\nCompatibility view created successfully!")


if __name__ == "__main__":
    main()
