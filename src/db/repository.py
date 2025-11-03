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
from typing import Iterable, Optional, Dict, Any, List
import sqlite3

from src.db.connection import transaction, connect
from src.db.row_utils import row_to_dict, rows_to_dicts


class BaseRepository:
    def __init__(self, conn: Optional[sqlite3.Connection] = None):
        self._conn = conn or connect()

    def execute(self, sql: str, params: Iterable = ()) -> List[Dict[str, Any]]:
        """
        Execute a statement inside a transaction and return fetched rows as dicts.
        Use this for write operations that must be transactional.
        
        Returns:
            List of dicts representing the rows, or empty list if no results
        """
        with transaction(self._conn) as cur:
            cur.execute(sql, tuple(params))
            try:
                rows = cur.fetchall()
                return rows_to_dicts(rows)
            except Exception:
                return []

    def fetchone(self, sql: str, params: Iterable = ()) -> Optional[Dict[str, Any]]:
        """
        Execute a query and return a single row as a dict.
        
        Returns:
            Dict representing the row, or None if no result
        """
        cur = self._conn.cursor()
        try:
            cur.execute(sql, tuple(params))
            row = cur.fetchone()
            return row_to_dict(row)
        finally:
            cur.close()

    def fetchall(self, sql: str, params: Iterable = ()) -> List[Dict[str, Any]]:
        """
        Execute a query and return all rows as a list of dicts.
        
        Returns:
            List of dicts representing the rows, or empty list if no results
        """
        cur = self._conn.cursor()
        try:
            cur.execute(sql, tuple(params))
            rows = cur.fetchall()
            return rows_to_dicts(rows)
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

    def get_member(self, member_id: int) -> Optional[Dict[str, Any]]:
        """Get a member by ID, returns dict or None."""
        return self.fetchone("SELECT * FROM members WHERE id = ?", (member_id,))

    def list_members(self) -> List[Dict[str, Any]]:
        """List all members, returns list of dicts."""
        return self.fetchall("SELECT * FROM members ORDER BY id")
