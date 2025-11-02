import tempfile
from pathlib import Path
from src.db.connection import connect, transaction

def test_connect_and_transaction(tmp_path):
    dbfile = tmp_path / "test.db"
    conn = connect(dbfile)
    # create table
    with transaction(conn) as cur:
        cur.execute("""CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT
        );""")
    # insert and read back
    with transaction(conn) as cur:
        cur.execute("INSERT INTO members (name, email) VALUES (?, ?)", ("Alice", "a@example.org"))
        last_id = cur.lastrowid
    # read using a fresh cursor (no transaction manager required for read)
    cur = conn.cursor()
    try:
        cur.execute("SELECT id, name, email FROM members WHERE id = ?", (last_id,))
        row = cur.fetchone()
        assert row is not None
        assert row["name"] == "Alice"
        assert row["email"] == "a@example.org"
    finally:
        cur.close()
