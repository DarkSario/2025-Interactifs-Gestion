from contextlib import contextmanager
import sqlite3
from pathlib import Path
import os

DB_DEFAULT_PATH = Path(os.getenv("APP_DB_PATH", "data/association.db"))

def _ensure_parent(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)

def connect(db_path: Path | str = None, timeout: float = 5.0) -> sqlite3.Connection:
    """
    Retourne une connexion sqlite3 configurée correctement.
    - active foreign keys
    - set busy_timeout
    - active WAL si possible (améliore concurrence)
    """
    path = DB_DEFAULT_PATH if db_path is None else Path(db_path)
    _ensure_parent(path)
    conn = sqlite3.connect(
        str(path),
        timeout=timeout,
        isolation_level=None,
        detect_types=sqlite3.PARSE_DECLTYPES,
    )
    # PRAGMAs conseillés
    try:
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.execute("PRAGMA synchronous = NORMAL;")
    except sqlite3.DatabaseError:
        # Certaines plateformes/versions peuvent refuser certains PRAGMA — ignorer en fallback
        pass
    # Connexion renvoie des rows nommés
    conn.row_factory = sqlite3.Row
    return conn

@contextmanager
def transaction(conn: sqlite3.Connection):
    """
    Context manager pour transaction:
    with transaction(conn) as cur:
        cur.execute(...)
    Commit / rollback automatique.
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