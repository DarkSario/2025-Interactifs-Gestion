from pathlib import Path
from src.db.connection import connect, transaction
try:
    from src.db.lock import db_file_lock
except Exception:
    try:
        from db.lock import db_file_lock  # type: ignore
    except Exception:
        db_file_lock = None

class InventoryService:
    def __init__(self, db_path: Path | str = None):
        self._db_path = db_path
        self._schema_cache = {}

    def _detect_table_names(self, cur):
        # Use cache if available
        if self._schema_cache:
            return (
                self._schema_cache['lines_table'],
                self._schema_cache['product_col'],
                self._schema_cache['qty_col'],
                self._schema_cache['inv_fk']
            )
        
        cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' "
            "AND name IN ('inventory_lines','inventaire_lignes','buvette_inventaire_lignes','inventory_line')"
        )
        found = [r[0] for r in cur.fetchall()]
        
        result = None
        if 'inventory_lines' in found:
            result = ('inventory_lines', 'product_id', 'qty', 'inventaire_id')
        elif 'inventaire_lignes' in found:
            result = ('inventaire_lignes', 'stock_id', 'quantite_constatee', 'inventaire_id')
        elif 'buvette_inventaire_lignes' in found:
            result = ('buvette_inventaire_lignes', 'article_id', 'quantite', 'inventaire_id')
        else:
            result = ('inventory_lines', 'product_id', 'qty', 'inventaire_id')
        
        # Cache the result
        self._schema_cache = {
            'lines_table': result[0],
            'product_col': result[1],
            'qty_col': result[2],
            'inv_fk': result[3]
        }
        return result

    def load_inventory_lines(self, inventaire_id: int):
        conn = connect(self._db_path)
        try:
            with transaction(conn) as cur:
                lines_table, product_col, qty_col, inv_fk = self._detect_table_names(cur)
                sql = (
                    f"SELECT id, {product_col} AS product_id, {qty_col} AS qty, {inv_fk} as inventaire_id "
                    f"FROM {lines_table} WHERE {inv_fk} = ? ORDER BY id"
                )
                cur.execute(sql, (inventaire_id,))
                rows = cur.fetchall()
                return [dict(r) for r in rows]
        finally:
            conn.close()

    def create_inventory(self, metadata: dict) -> int:
        db_path = self._db_path or "association.db"
        lock_ctx = db_file_lock if db_file_lock is not None else (lambda *_args, **_kwargs: (lambda: (yield)))
        with lock_ctx(db_path):
            conn = connect(self._db_path)
            try:
                with transaction(conn) as cur:
                    # Detect which inventory table exists
                    cur.execute(
                        "SELECT name FROM sqlite_master WHERE type='table' "
                        "AND name IN ('inventaires','buvette_inventaires','inventories')"
                    )
                    found = [r[0] for r in cur.fetchall()]
                    
                    # Check what columns the table has
                    table_name = 'inventaires'
                    if 'buvette_inventaires' in found:
                        table_name = 'buvette_inventaires'
                    elif not found:
                        table_name = 'inventaires'  # default
                    
                    # Get columns for the table
                    cur.execute(f"PRAGMA table_info({table_name})")
                    columns = [row[1] for row in cur.fetchall()]
                    
                    # Build INSERT based on available columns
                    if 'name' in columns:
                        # New schema with 'name' column
                        cur.execute(
                            f"INSERT INTO {table_name} (name, created_at) VALUES (?, CURRENT_TIMESTAMP)",
                            (metadata.get("name", ""),)
                        )
                    elif 'date_inventaire' in columns:
                        # Legacy schema with date_inventaire
                        cur.execute(
                            f"INSERT INTO {table_name} (date_inventaire, event_id, commentaire) VALUES (CURRENT_TIMESTAMP, ?, ?)",
                            (metadata.get("event_id"), metadata.get("commentaire", ""))
                        )
                    else:
                        # Minimal fallback
                        cur.execute(f"INSERT INTO {table_name} DEFAULT VALUES")
                    
                    new_id = cur.lastrowid
                return new_id
            finally:
                conn.close()
