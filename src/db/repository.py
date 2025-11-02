"""
BaseRepository et exemples de repositories métier.

Usage:
    from src.db.connection import connect
    from src.db.repository import MembersRepository

    conn = connect("data/association.db")
    repo = MembersRepository(conn)
    member_id = repo.create_member("Alice", "a@example.org")
    row = repo.get_member(member_id)
"""
from typing import Iterable, Optional, Any
import sqlite3

from src.db.connection import transaction, connect


class BaseRepository:
    def __init__(self, conn: Optional[sqlite3.Connection] = None):
        self._conn = conn or connect()

    def execute(self, sql: str, params: Iterable = ()):
        """
        Execute a statement inside a transaction and return fetched rows.
        Use this for write operations that must be transactional.
        """
        with transaction(self._conn) as cur:
            cur.execute(sql, tuple(params))
            try:
                return cur.fetchall()
            except Exception:
                return []

    def fetchone(self, sql: str, params: Iterable = ()):
        cur = self._conn.cursor()
        try:
            cur.execute(sql, tuple(params))
            return cur.fetchone()
        finally:
            cur.close()

    def fetchall(self, sql: str, params: Iterable = ()):
        cur = self._conn.cursor()
        try:
            cur.execute(sql, tuple(params))
            return cur.fetchall()
        finally:
            cur.close()


class MembersRepository(BaseRepository):
    def ensure_table(self):
        with transaction(self._conn) as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS members (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT
                );
                """
            )

    def create_member(self, name: str, email: str) -> int:
        with transaction(self._conn) as cur:
            cur.execute(
                "INSERT INTO members (name, email) VALUES (?, ?)",
                (name, email),
            )
            return cur.lastrowid

    def get_member(self, member_id: int) -> Optional[sqlite3.Row]:
        return self.fetchone("SELECT * FROM members WHERE id = ?", (member_id,))

    def list_members(self):
        return self.fetchall("SELECT * FROM members ORDER BY id")
