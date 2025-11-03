"""
Connexion et context manager transaction pour SQLite.

Usage:
    from src.db.connection import connect, transaction, set_busy_timeout

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

DEFAULT_BUSY_TIMEOUT_MS = int(os.getenv("DB_BUSY_TIMEOUT_MS", "5000"))


def _ensure_parent(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)


def connect(
    db_path: Path | str = None,
    timeout: float = 5.0,
    check_same_thread: bool = True
) -> sqlite3.Connection:
    """
    Retourne une connexion sqlite3 configurée.
    - Active foreign_keys
    - Active WAL (améliore concurrence lecture/écriture)
    - Définit row_factory sur sqlite3.Row pour accès par clé
    - Définit PRAGMA busy_timeout afin que sqlite attende au lieu
      d'échouer immédiatement
    """
    path = DB_DEFAULT_PATH if db_path is None else Path(db_path)
    _ensure_parent(path)
    # isolation_level=None => autocommit mode, use explicit BEGIN
    # in transaction()
    conn = sqlite3.connect(
        str(path),
        timeout=timeout,
        isolation_level=None,
        detect_types=sqlite3.PARSE_DECLTYPES,
        check_same_thread=check_same_thread,
    )
    # Ensure PRAGMAs for safer concurrency
    conn.execute("PRAGMA foreign_keys = ON;")
    try:
        conn.execute("PRAGMA journal_mode = WAL;")
    except Exception:
        pass
    conn.execute("PRAGMA synchronous = NORMAL;")
    conn.execute(f"PRAGMA busy_timeout = {DEFAULT_BUSY_TIMEOUT_MS};")
    conn.row_factory = sqlite3.Row
    return conn


def set_busy_timeout(conn: sqlite3.Connection, ms: int) -> None:
    """Set busy timeout (ms) on a live connection."""
    try:
        conn.execute(f"PRAGMA busy_timeout = {int(ms)};")
    except Exception:
        # tolerate failures in restricted environments
        pass


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
        # BEGIN is used with isolation_level=None (autocommit)
        # to start a transaction
        cur.execute("BEGIN")
        yield cur
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
