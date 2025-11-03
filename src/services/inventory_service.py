from pathlib import Path
from src.db.connection import connect, transaction
from src.db.lock import db_file_lock


class InventoryService:
    def __init__(self, db_path: Path | str = None):
        self._db_path = db_path

    def load_inventory_lines(self, inventaire_id: int):
        """Load inventory lines for editing. Uses a single connection +
        transaction to get consistent results."""
        conn = connect(self._db_path)
        try:
            with transaction(conn) as cur:
                cur.execute(
                    "SELECT id, product_id, qty FROM inventory_lines "
                    "WHERE inventaire_id = ? ORDER BY id",
                    (inventaire_id,)
                )
                rows = cur.fetchall()
                # convert to list of dicts to detach from cursor/connection
                return [dict(r) for r in rows]
        finally:
            conn.close()

    def create_inventory(self, metadata: dict) -> int:
        """Create a new inventory in an exclusive lock to avoid concurrent
        schema/insert races that can cause DB locked errors.

        This method takes an exclusive db_file_lock while performing the
        create to serialise competing creators in multi-process setups.
        """
        db_path = self._db_path or "data/association.db"
        # Acquire a cross-process lock for the DB path; portalocker will
        # block until lock acquired.
        with db_file_lock(db_path):
            conn = connect(self._db_path)
            try:
                with transaction(conn) as cur:
                    cur.execute(
                        "INSERT INTO inventaires (name, created_at) "
                        "VALUES (?, CURRENT_TIMESTAMP)",
                        (metadata.get("name", ""),)
                    )
                    new_id = cur.lastrowid
                return new_id
            finally:
                conn.close()
