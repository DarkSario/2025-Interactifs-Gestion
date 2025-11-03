import sys
import sqlite3
from pathlib import Path

# Mock tkinter before any imports that might use it
sys.modules['tkinter'] = type(sys)('tkinter')
sys.modules['tkinter.messagebox'] = type(sys)('messagebox')

from db.db import get_connection
from modules.buvette_inventaire_db import delete_inventaire

def test_delete_inventaire_with_children(tmp_path):
    import os
    
    dbfile = tmp_path / "test_inv.db"
    # Create DB file at dbfile path by connecting directly to that file
    conn = sqlite3.connect(str(dbfile))
    conn.row_factory = sqlite3.Row
    try:
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS buvette_inventaires (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date_inventaire TEXT,
                event_id INTEGER,
                commentaire TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS buvette_inventaire_lignes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                inventaire_id INTEGER,
                article_id INTEGER,
                quantite INTEGER,
                FOREIGN KEY (inventaire_id) REFERENCES buvette_inventaires(id)
            )
        """)
        conn.commit()
    finally:
        conn.close()

    # Use db.db.get_connection shim to point to this tmp db for the test
    # Save original value to restore later
    original_db_path = os.environ.get("APP_DB_PATH")
    try:
        os.environ["APP_DB_PATH"] = str(dbfile)

        # Insert parent and children via get_connection
        conn2 = get_connection()
        try:
            with conn2:
                cur = conn2.execute("INSERT INTO buvette_inventaires (date_inventaire) VALUES (CURRENT_TIMESTAMP)")
                inv_id = cur.lastrowid
                conn2.execute("INSERT INTO buvette_inventaire_lignes (inventaire_id, article_id, quantite) VALUES (?, ?, ?)", (inv_id, 1, 5))
        finally:
            conn2.close()

        # Call delete_inventaire
        delete_inventaire(inv_id)

        # Verify parent and children removed using direct sqlite3 to the tmp file
        conn3 = sqlite3.connect(str(dbfile))
        try:
            conn3.row_factory = sqlite3.Row
            cur = conn3.execute("SELECT COUNT(*) FROM buvette_inventaires WHERE id = ?", (inv_id,))
            assert cur.fetchone()[0] == 0
            cur = conn3.execute("SELECT COUNT(*) FROM buvette_inventaire_lignes WHERE inventaire_id = ?", (inv_id,))
            assert cur.fetchone()[0] == 0
        finally:
            conn3.close()
    finally:
        # Restore original environment variable
        if original_db_path is None:
            os.environ.pop("APP_DB_PATH", None)
        else:
            os.environ["APP_DB_PATH"] = original_db_path
