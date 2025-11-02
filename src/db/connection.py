"""
Connexion et context manager transaction pour SQLite.

Usage:
    from src.db.connection import connect, transaction

    conn = connect()
    with transaction(conn) as cur:
        cur.execute("CREATE TABLE IF NOT EXISTS x (id INTEGER PRIMARY KEY, name TEXT)")
        cur.execute("INSERT INTO x (name) VALUES (?)", ("Alice",))
"""
from contextlib import contextmanager
import sqlite3
from pathlib import Path
import os

DB_DEFAULT_PATH = Path(os.getenv("APP_DB_PATH", "data/association.db"))

def _ensure_parent(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)

def connect(db_path: Path | str = None, timeout: float = 5.0) -> sqlite3.Connection:
    """
    Retourne une connexion sqlite3 configurée.
    - Active foreign_keys
    - Active WAL (améliore concurrence lecture/écriture)
    - Définit row_factory sur sqlite3.Row pour accès par clé
    """
    path = DB_DEFAULT_PATH if db_path is None else Path(db_path)
    _ensure_parent(path)
    conn = sqlite3.connect(str(path), timeout=timeout, isolation_level=None, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.execute("PRAGMA foreign_keys = ON;")
    # journal_mode pragma peut échouer sur certains environnements -> ignore errors silently
    try:
        conn.execute("PRAGMA journal_mode = WAL;")
    except Exception:
        pass
    conn.execute("PRAGMA synchronous = NORMAL;")
    conn.row_factory = sqlite3.Row
    return conn

@contextmanager
def transaction(conn: sqlite3.Connection):
    """
    Context manager pour les transactions :
    with transaction(conn) as cur:
        cur.execute(...)
    Commit si OK, rollback si exception.
    """
    cur = conn.cursor()
    try:
        cur.execute("BEGIN")
        yield cur
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()