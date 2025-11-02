import sys
from pathlib import Path

# Ensure src/ is on sys.path for tests when using src layout
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from src.db.connection import connect
from src.db.repository import MembersRepository

def test_member_create_and_fetch(tmp_path):
    dbfile = tmp_path / "test.db"
    conn = connect(dbfile)
    cur = conn.cursor()
    cur.execute(
        """CREATE TABLE members (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT);"""
    )
    conn.commit()
    repo = MembersRepository(conn)
    mid = repo.create_member("Alice", "alice@example.org")
    rec = repo.get_member(mid)
    assert rec["name"] == "Alice"
    assert rec["email"] == "alice@example.org"