"""Compatibility shim to unify DB API.

Exposes legacy API: get_connection, set_db_file, get_db_file, transaction.
Delegates to src.db.connection.connect when available to ensure WAL and busy_timeout
are applied project-wide.
"""
import os
from pathlib import Path
from typing import Optional
try:
    from src.db.connection import connect as _connect, transaction as _transaction, DB_DEFAULT_PATH  # type: ignore
except Exception:
    _connect = None
    _transaction = None
    DB_DEFAULT_PATH = Path(os.getenv("APP_DB_PATH", "association.db"))


def set_db_file(path: str) -> None:
    os.environ["APP_DB_PATH"] = str(path)


def get_db_file() -> str:
    return os.getenv("APP_DB_PATH", str(DB_DEFAULT_PATH))


def get_connection(path: Optional[str] = None, **kwargs):
    """Return a connection using the canonical connect implementation if available,
    otherwise fallback to sqlite3.connect (with reasonable PRAGMAs).
    """
    if _connect is not None:
        return _connect(path)
    # Fallback minimal:
    import sqlite3
    p = path or get_db_file()
    p = str(p)
    _conn = sqlite3.connect(p, timeout=5, detect_types=sqlite3.PARSE_DECLTYPES)
    _conn.row_factory = sqlite3.Row
    try:
        _conn.execute("PRAGMA journal_mode=WAL;")
        _conn.execute("PRAGMA busy_timeout=5000;")
    except Exception:
        pass
    return _conn


def transaction(conn):
    if _transaction is not None:
        return _transaction(conn)
    # basic fallback contextmanager:
    from contextlib import contextmanager
    @contextmanager
    def _txn(c):
        cur = c.cursor()
        try:
            cur.execute("BEGIN")
            yield cur
            c.commit()
        except Exception:
            c.rollback()
            raise
        finally:
            cur.close()
    return _txn(conn)
