from pathlib import Path
from src.db.connection import connect, transaction, DB_DEFAULT_PATH
from src.db.lock import db_file_lock


class InventoryService:
    def __init__(self, db_path: Path | str = None):
        self._db_path = db_path
        # Cache for detected schema
        self._schema_cache = {}

    def _detect_schema(self, conn) -> dict:
        """Detect the actual table and column names in the database.
        
        Returns a dict with keys:
        - lines_table: name of inventory lines table
        - product_id_col: name of product/article ID column
        - qty_col: name of quantity column
        - inventaire_id_col: name of inventory ID column
        """
        if self._schema_cache:
            return self._schema_cache
            
        cur = conn.cursor()
        
        # Try to find the inventory lines table
        cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND "
            "(name='inventory_lines' OR name='inventaire_lignes' OR name='buvette_inventaire_lignes')"
        )
        table_row = cur.fetchone()
        
        if not table_row:
            # Default fallback
            schema = {
                'lines_table': 'inventory_lines',
                'product_id_col': 'product_id',
                'qty_col': 'qty',
                'inventaire_id_col': 'inventaire_id'
            }
            self._schema_cache = schema
            return schema
            
        lines_table = table_row[0]
        
        # Get column names for the table
        cur.execute(f"PRAGMA table_info({lines_table})")
        columns = [row[1] for row in cur.fetchall()]
        
        # Map column names
        product_id_col = 'product_id'
        if 'article_id' in columns:
            product_id_col = 'article_id'
        elif 'stock_id' in columns:
            product_id_col = 'stock_id'
            
        qty_col = 'qty'
        if 'quantite' in columns:
            qty_col = 'quantite'
        elif 'quantite_constatee' in columns:
            qty_col = 'quantite_constatee'
            
        inventaire_id_col = 'inventaire_id'
        
        schema = {
            'lines_table': lines_table,
            'product_id_col': product_id_col,
            'qty_col': qty_col,
            'inventaire_id_col': inventaire_id_col
        }
        self._schema_cache = schema
        return schema

    def load_inventory_lines(self, inventaire_id: int):
        """Load inventory lines for editing. Uses a single connection +
        transaction to get consistent results.
        
        Automatically detects schema table and column names to support
        both legacy (inventaire_lignes, stock_id, quantite_constatee) and
        new (inventory_lines, product_id, qty) schemas.
        """
        conn = connect(self._db_path)
        try:
            schema = self._detect_schema(conn)
            
            with transaction(conn) as cur:
                query = (
                    f"SELECT id, {schema['product_id_col']} as product_id, "
                    f"{schema['qty_col']} as qty FROM {schema['lines_table']} "
                    f"WHERE {schema['inventaire_id_col']} = ? ORDER BY id"
                )
                cur.execute(query, (inventaire_id,))
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
        db_path = self._db_path or DB_DEFAULT_PATH
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
