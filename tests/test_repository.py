from pathlib import Path
from src.db.connection import connect
from src.db.repository import MembersRepository


def test_members_repository_crud(tmp_path):
    dbfile = tmp_path / "repo_test.db"
    conn = connect(dbfile)
    repo = MembersRepository(conn)

    # ensure table creation works
    repo.ensure_table()

    # insert
    mid = repo.create_member("Bob", "bob@example.org")
    assert isinstance(mid, int)

    # fetch
    rec = repo.get_member(mid)
    assert rec is not None
    assert rec["name"] == "Bob"
    assert rec["email"] == "bob@example.org"

    # list
    items = repo.list_members()
    assert len(items) >= 1
