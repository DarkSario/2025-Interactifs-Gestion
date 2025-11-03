"""
Module de gestion de la base de données pour les inventaires de la buvette.

STANDARDIZATION (PR copilot/audit-db-access-standardization):
- Improved connection management with try/finally blocks to reduce locks
- Converted sqlite3.Row to dicts for consistent .get() access patterns
- Added docstrings and error handling

STOCK MANAGEMENT (PR fix/stock-and-unite):
- Added revert_inventory_effect call in delete_inventaire to prevent FK constraint failures
- Added apply_inventory_snapshot_wrapper helper for inventory create/update flows
"""

from db.db import get_connection
from utils.db_helpers import rows_to_dicts, row_to_dict
from utils.app_logger import get_logger
from modules.stock_db import (
    revert_inventory_effect, apply_inventory_snapshot
)
import sqlite3

logger = get_logger("buvette_inventaire_db")

def get_conn():
    conn = get_connection()
    return conn

# ----- INVENTAIRES -----
def list_inventaires():
    """List all inventaires with event info, returns list of dicts."""
    conn = None
    try:
        conn = get_conn()
        rows = conn.execute("""
            SELECT i.*, e.name as event_name, e.date as event_date
            FROM buvette_inventaires i
            LEFT JOIN events e ON i.event_id = e.id
            ORDER BY date_inventaire DESC
        """).fetchall()
        return rows_to_dicts(rows)
    finally:
        if conn:
            conn.close()

def get_inventaire_by_id(inv_id):
    """Get inventaire by ID with event info, returns dict or None."""
    conn = None
    try:
        conn = get_conn()
        row = conn.execute("""
            SELECT i.*, e.name as event_name, e.date as event_date
            FROM buvette_inventaires i
            LEFT JOIN events e ON i.event_id = e.id
            WHERE i.id=?
        """, (inv_id,)).fetchone()
        return row_to_dict(row)
    finally:
        if conn:
            conn.close()

def insert_inventaire(date_inventaire, event_id, type_inventaire, commentaire):
    """Insert new inventaire, returns ID of created record."""
    conn = None
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO buvette_inventaires (date_inventaire, event_id, type_inventaire, commentaire)
            VALUES (?, ?, ?, ?)
        """, (date_inventaire, event_id, type_inventaire, commentaire))
        inv_id = cur.lastrowid
        conn.commit()
        return inv_id
    finally:
        if conn:
            conn.close()

def update_inventaire(inv_id, date_inventaire, event_id, type_inventaire, commentaire):
    """Update existing inventaire."""
    conn = None
    try:
        conn = get_conn()
        conn.execute("""
            UPDATE buvette_inventaires SET date_inventaire=?, event_id=?, type_inventaire=?, commentaire=?
            WHERE id=?
        """, (date_inventaire, event_id, type_inventaire, commentaire, inv_id))
        conn.commit()
    finally:
        if conn:
            conn.close()

def _find_referencing_tables(conn, parent_table):
    """Return list of tuples (table_name, from_column) for tables that have a FK to parent_table.
    
    Note: Table names come from sqlite_master and are trusted. Column names come from PRAGMA.
    """
    cur = conn.cursor()
    try:
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [r[0] for r in cur.fetchall()]
        refs = []
        for t in tables:
            # Table name comes from sqlite_master system table, is safe to use in PRAGMA
            try:
                fk_rows = conn.execute(f"PRAGMA foreign_key_list({t})").fetchall()
            except Exception:
                fk_rows = []
            # fk_rows columns: (id, seq, table, from, to, on_update, on_delete, match)
            for fk in fk_rows:
                # Some SQLite returns rows as sqlite3.Row; index accordingly
                try:
                    referenced_table = fk[2]
                    from_col = fk[3]
                except Exception:
                    # fallback if row-like access differs
                    referenced_table = fk["table"] if "table" in fk.keys() else fk[2]
                    from_col = fk["from"] if "from" in fk.keys() else fk[3]
                if referenced_table == parent_table:
                    refs.append((t, from_col))
        return refs
    finally:
        cur.close()

def delete_inventaire(inv_id):
    """Supprime un inventaire de façon sûre: annule les effets stock, supprime les lignes enfants, puis l'inventaire."""
    conn = None
    try:
        # First, revert inventory effects on stock to maintain consistency
        try:
            revert_inventory_effect(inv_id)
            logger.info(f"Reverted stock effects for inventory {inv_id}")
        except Exception as e:
            logger.warning(
                f"Could not revert stock effects for inventory {inv_id}: {e}"
            )

        conn = get_conn()
        # Ensure foreign keys enforcement (defensive)
        try:
            conn.execute("PRAGMA foreign_keys = ON;")
        except Exception:
            pass

        # Discover tables referencing the parent table
        refs = _find_referencing_tables(conn, "buvette_inventaires")

        # Begin explicit transaction
        cur = conn.cursor()
        try:
            cur.execute("BEGIN")
            # Delete from child tables first
            for (table, fk_col) in refs:
                logger.info("Deleting child rows in %s where %s = %s", table, fk_col, str(inv_id))
                # Table and column names come from sqlite_master/PRAGMA, are trusted system sources
                cur.execute(f"DELETE FROM {table} WHERE {fk_col} = ?", (inv_id,))
            # Finally delete the parent
            cur.execute("DELETE FROM buvette_inventaires WHERE id = ?", (inv_id,))
            conn.commit()
            logger.info("Deleted inventaire id=%s and %d child table deletions", inv_id, len(refs))
        except Exception:
            conn.rollback()
            raise
        finally:
            cur.close()
    finally:
        if conn:
            conn.close()

# ----- LIGNES D'INVENTAIRE -----
def list_lignes_inventaire(inventaire_id):
    """List inventory lines for specific inventory with article names, returns list of dicts."""
    conn = None
    try:
        conn = get_conn()
        rows = conn.execute("""
            SELECT l.*, a.name as article_name
            FROM buvette_inventaire_lignes l
            LEFT JOIN buvette_articles a ON l.article_id = a.id
            WHERE l.inventaire_id=?
            ORDER BY a.name
        """, (inventaire_id,)).fetchall()
        return rows_to_dicts(rows)
    finally:
        if conn:
            conn.close()

def insert_ligne_inventaire(inventaire_id, article_id, quantite, commentaire=None):
    """Insert new inventory line."""
    conn = None
    try:
        conn = get_conn()
        conn.execute("""
            INSERT INTO buvette_inventaire_lignes (inventaire_id, article_id, quantite, commentaire)
            VALUES (?, ?, ?, ?)
        """, (inventaire_id, article_id, quantite, commentaire))
        conn.commit()
    finally:
        if conn:
            conn.close()

def update_ligne_inventaire(ligne_id, article_id, quantite, commentaire=None):
    """Update existing inventory line."""
    conn = None
    try:
        conn = get_conn()
        conn.execute("""
            UPDATE buvette_inventaire_lignes SET article_id=?, quantite=?, commentaire=?
            WHERE id=?
        """, (article_id, quantite, commentaire, ligne_id))
        conn.commit()
    finally:
        if conn:
            conn.close()

def delete_ligne_inventaire(ligne_id):
    """Delete inventory line by ID."""
    conn = None
    try:
        conn = get_conn()
        conn.execute("DELETE FROM buvette_inventaire_lignes WHERE id=?", (ligne_id,))
        conn.commit()
    finally:
        if conn:
            conn.close()

def upsert_ligne_inventaire(inventaire_id, article_id, quantite, commentaire=None):
    """Insert or update inventory line for article in inventory."""
    conn = None
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            SELECT id FROM buvette_inventaire_lignes WHERE inventaire_id=? AND article_id=?
        """, (inventaire_id, article_id))
        row = cur.fetchone()
        if row:
            cur.execute("""
                UPDATE buvette_inventaire_lignes SET quantite=?, commentaire=?
                WHERE inventaire_id=? AND article_id=?
            """, (quantite, commentaire, inventaire_id, article_id))
        else:
            cur.execute("""
                INSERT INTO buvette_inventaire_lignes (inventaire_id, article_id, quantite, commentaire)
                VALUES (?, ?, ?, ?)
            """, (inventaire_id, article_id, quantite, commentaire))
        conn.commit()
    finally:
        if conn:
            conn.close()

# ----- EVENEMENTS UTILITY -----
def list_events():
    """List events for dropdown, returns list of dicts."""
    conn = None
    try:
        conn = get_conn()
        rows = conn.execute("SELECT id, name FROM events ORDER BY date DESC").fetchall()
        return rows_to_dicts(rows)
    finally:
        if conn:
            conn.close()


# ----- STOCK INTEGRATION -----
def apply_inventory_snapshot_wrapper(inv_id):
    """
    Helper pour appliquer un snapshot d'inventaire au stock.

    Cette fonction doit être appelée après la création ou la mise à jour d'un inventaire
    pour mettre à jour automatiquement les stocks des articles.

    Args:
        inv_id: ID de l'inventaire dont il faut appliquer les quantités au stock

    Example usage in inventory create flow:
        inv_id = insert_inventaire(date, event_id, type_inv, comment)
        # ... insert inventory lines ...
        apply_inventory_snapshot_wrapper(inv_id)
    """
    conn = None
    try:
        conn = get_conn()
        # Get all inventory lines for this inventory
        rows = conn.execute("""
            SELECT article_id, quantite
            FROM buvette_inventaire_lignes
            WHERE inventaire_id=?
        """, (inv_id,)).fetchall()

        snapshot = [{"article_id": row[0], "quantite": row[1]} for row in rows]

        if snapshot:
            apply_inventory_snapshot(inv_id, snapshot)
            logger.info(f"Applied inventory snapshot for inventory {inv_id}")
        else:
            logger.warning(
                f"No inventory lines found for inventory {inv_id}, "
                f"skipping stock update"
            )
    except Exception as e:
        logger.error(
            f"Error applying inventory snapshot wrapper for "
            f"inventory {inv_id}: {e}"
        )
        raise
    finally:
        if conn:
            conn.close()
