from typing import Iterable, Any
from .connection import connect, transaction
import sqlite3


class BaseRepository:
    def __init__(self, conn: sqlite3.Connection | None = None):
        self._conn = conn or connect()

    def execute(self, sql: str, params: Iterable = ()): 
        with transaction(self._conn) as cur:
            cur.execute(sql, tuple(params))
            return cur.fetchall()

    def fetchone(self, sql: str, params: Iterable = ()): 
        cur = self._conn.cursor()
        try:
            cur.execute(sql, tuple(params))
            return cur.fetchone()
        finally:
            cur.close()


class MembersRepository(BaseRepository):
    def create_member(self, name: str, email: str) -> int:
        sql = "INSERT INTO members (name, email) VALUES (?, ?)"
        with transaction(self._conn) as cur:
            cur.execute(sql, (name, email))
            return cur.lastrowid

    def get_member(self, member_id: int):
        return self.fetchone("SELECT * FROM members WHERE id = ?", (member_id,))