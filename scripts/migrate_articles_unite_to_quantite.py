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
            prix_achat REAL
        );
        """)

        # Detect existing columns and map known columns into new structure
        old_cols = [r[1] for r in conn.execute("PRAGMA table_info(buvette_articles)").fetchall()]
        print("Old columns:", old_cols)

        # Build SELECT that maps unite -> unite_type and other known columns
        select_parts = []
        # Ensure order: id, name, categorie, unite AS unite_type, contenance, commentaire, prix_achat
        if "id" in old_cols: select_parts.append("id")
        if "name" in old_cols: select_parts.append("name")
        if "categorie" in old_cols: select_parts.append("categorie")
        if "unite" in old_cols: select_parts.append("unite AS unite_type")
        else: select_parts.append("NULL AS unite_type")
        if "contenance" in old_cols: select_parts.append("contenance")
        else: select_parts.append("NULL AS contenance")
        if "commentaire" in old_cols: select_parts.append("commentaire")
        else: select_parts.append("NULL AS commentaire")
        if "prix_achat" in old_cols:
            select_parts.append("prix_achat")
        elif "prix" in old_cols:
            select_parts.append("prix AS prix_achat")
        else:
            select_parts.append("NULL AS prix_achat")

        select_sql = ", ".join(select_parts)
        copy_sql = f"INSERT INTO buvette_articles_new (id, name, categorie, unite_type, contenance, commentaire, prix_achat) SELECT {select_sql} FROM buvette_articles;"
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
