"""
Migration: remove column 'unite' from buvette_articles and add numeric 'quantite' column.
- Backs up DB to <db>.bak before applying changes.
- Preserves legacy 'unite' values into 'unite_type' column in the new table.
Usage:
    python scripts/migrate_articles_unite_to_quantite.py --db path/to/association.db
"""
import sqlite3
import shutil
import argparse
from pathlib import Path

def table_has_column(conn, table, column):
    # Table name is validated by checking it exists in sqlite_master
    cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,))
    if not cur.fetchone():
        raise ValueError(f"Table {table} does not exist")
    # Now safe to use in PRAGMA since it's confirmed to exist
    cur = conn.execute(f"PRAGMA table_info({table})")
    cols = [r[1] for r in cur.fetchall()]
    return column in cols

def backup(db_path):
    bak = str(db_path) + ".bak"
    shutil.copy2(db_path, bak)
    print(f"Backup created: {bak}")

def migrate(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        # ensure foreign keys enforcement
        try:
            conn.execute("PRAGMA foreign_keys = ON;")
        except Exception:
            pass

        if not table_has_column(conn, "buvette_articles", "unite"):
            print("No 'unite' column found in buvette_articles, nothing to do.")
            return

        print("Starting migration: creating buvette_articles_new ...")
        cur = conn.cursor()
        cur.execute("BEGIN")

        # Create new table: adapt columns to match your real schema if needed
        cur.execute("""
        CREATE TABLE buvette_articles_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            categorie TEXT,
            quantite INTEGER DEFAULT 0,
            unite_type TEXT,
            contenance TEXT,
            commentaire TEXT,
            stock INTEGER DEFAULT 0,
            purchase_price REAL
        );
        """)

        # Detect existing columns and map known columns into new structure
        old_cols = [r[1] for r in conn.execute("PRAGMA table_info(buvette_articles)").fetchall()]
        print("Old columns:", old_cols)

        # Build both INSERT columns and SELECT expressions dynamically
        insert_cols = []
        select_parts = []
        
        # id - always include if present
        if "id" in old_cols:
            insert_cols.append("id")
            select_parts.append("id")
        
        # name - required field
        if "name" in old_cols:
            insert_cols.append("name")
            select_parts.append("name")
        
        # categorie - optional
        if "categorie" in old_cols:
            insert_cols.append("categorie")
            select_parts.append("categorie")
        
        # unite -> unite_type
        if "unite" in old_cols:
            insert_cols.append("unite_type")
            select_parts.append("unite AS unite_type")
        
        # contenance - optional
        if "contenance" in old_cols:
            insert_cols.append("contenance")
            select_parts.append("contenance")
        
        # commentaire - optional
        if "commentaire" in old_cols:
            insert_cols.append("commentaire")
            select_parts.append("commentaire")
        
        # stock - optional
        if "stock" in old_cols:
            insert_cols.append("stock")
            select_parts.append("stock")
        
        # purchase_price or prix_achat or prix - optional
        if "purchase_price" in old_cols:
            insert_cols.append("purchase_price")
            select_parts.append("purchase_price")
        elif "prix_achat" in old_cols:
            insert_cols.append("purchase_price")
            select_parts.append("prix_achat AS purchase_price")
        elif "prix" in old_cols:
            insert_cols.append("purchase_price")
            select_parts.append("prix AS purchase_price")

        insert_sql = ", ".join(insert_cols)
        select_sql = ", ".join(select_parts)
        copy_sql = f"INSERT INTO buvette_articles_new ({insert_sql}) SELECT {select_sql} FROM buvette_articles;"
        try:
            cur.execute(copy_sql)
        except Exception as e:
            print("Copy failed, aborting:", e)
            conn.rollback()
            return

        cur.execute("DROP TABLE buvette_articles;")
        cur.execute("ALTER TABLE buvette_articles_new RENAME TO buvette_articles;")
        conn.commit()
        print("Migration completed: buvette_articles updated.")
    finally:
        conn.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default="association.db", help="Path to sqlite DB")
    args = parser.parse_args()
    db_path = Path(args.db)
    if not db_path.exists():
        print("DB not found:", db_path)
        return
    backup(db_path)
    migrate(str(db_path))

if __name__ == "__main__":
    main()
