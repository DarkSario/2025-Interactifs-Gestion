"""
Module de gestion du stock avec journal des modifications.

Ce module fournit:
- ensure_stock_tables(): création des tables nécessaires pour le journal
- get_stock(article_id): récupération du stock actuel d'un article
- set_stock(article_id, quantity): mise à jour directe du stock
- adjust_stock(article_id, delta, reason): ajustement avec traçabilité
- apply_inventory_snapshot(inv_id, snapshot): applique un inventaire et
  enregistre les deltas
- revert_inventory_effect(inv_id): annule les effets d'un inventaire
- inventory_stock_journal(inv_id): récupère l'historique des modifications

Toutes les opérations sont transactionnelles.
"""

from db.db import get_connection
from utils.db_helpers import rows_to_dicts
from utils.app_logger import get_logger

logger = get_logger("stock_db")


def ensure_stock_tables(conn=None):
    """
    Crée la table inventory_stock_journal si elle n'existe pas.
    Cette table enregistre les modifications de stock liées aux inventaires.
    
    Args:
        conn: Optional database connection. If None, creates a new connection.
    """
    conn_provided = conn is not None
    if not conn_provided:
        conn = get_connection()
    
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS inventory_stock_journal (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                inventaire_id INTEGER,
                achat_id INTEGER,
                article_id INTEGER NOT NULL,
                delta INTEGER NOT NULL,
                scope TEXT DEFAULT 'buvette',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (inventaire_id) REFERENCES buvette_inventaires(id),
                FOREIGN KEY (article_id) REFERENCES buvette_articles(id)
            )
        """)
        if not conn_provided:
            conn.commit()
        logger.info("inventory_stock_journal table created/verified")
    except Exception as e:
        logger.error(f"Error ensuring stock tables: {e}")
        if not conn_provided and conn:
            conn.rollback()
        raise
    finally:
        if not conn_provided and conn:
            conn.close()


def get_stock(conn, article_id):
    """
    Récupère le stock actuel d'un article.

    Args:
        conn: Database connection
        article_id: ID de l'article

    Returns:
        int: Stock actuel (0 si l'article n'existe pas ou n'a pas de stock)
    """
    try:
        row = conn.execute(
            "SELECT stock FROM buvette_articles WHERE id=?",
            (article_id,)
        ).fetchone()
        if row:
            return row[0] if row[0] is not None else 0
        return 0
    except Exception as e:
        logger.error(f"Error getting stock for article {article_id}: {e}")
        return 0


def set_stock(conn, article_id, qty):
    """
    Met à jour le stock d'un article à une valeur absolue.

    Args:
        conn: Database connection
        article_id: ID de l'article
        qty: Nouvelle quantité en stock
    """
    try:
        conn.execute(
            "UPDATE buvette_articles SET stock=? WHERE id=?",
            (qty, article_id)
        )
        logger.debug(f"Set stock for article {article_id} to {qty}")
    except Exception as e:
        logger.error(f"Error setting stock for article {article_id}: {e}")
        raise


def adjust_stock(conn, article_id, delta, reason=None):
    """
    Ajuste le stock d'un article par un delta (positif ou négatif).

    Args:
        conn: Database connection
        article_id: ID de l'article
        delta: Quantité à ajouter (positif) ou retirer (négatif)
        reason: Motif de l'ajustement (optionnel)
    """
    try:
        current_stock = get_stock(conn, article_id)
        new_stock = max(0, current_stock + delta)
        set_stock(conn, article_id, new_stock)
        logger.info(
            f"Adjusted stock for article {article_id} by {delta} "
            f"(reason: {reason})"
        )
    except Exception as e:
        logger.error(f"Error adjusting stock for article {article_id}: {e}")
        raise


def apply_inventory_snapshot(conn, inventaire_id, lines_table_candidates=None):
    """
    Applique un snapshot d'inventaire et enregistre les deltas.

    Args:
        conn: Database connection
        inventaire_id: ID de l'inventaire
        lines_table_candidates: Optional list of table names to search for inventory lines.
                               Defaults to ['buvette_inventaire_lignes']

    Cette fonction:
    1. Récupère les lignes d'inventaire depuis les tables candidates
    2. Calcule le delta entre le stock actuel et la quantité inventoriée
    3. Met à jour le stock de chaque article
    4. Enregistre les deltas dans inventory_stock_journal pour annulation
    """
    if lines_table_candidates is None:
        lines_table_candidates = ['buvette_inventaire_lignes']
    
    try:
        cursor = conn.cursor()
        
        # Find inventory lines from candidate tables
        snapshot = []
        for table_name in lines_table_candidates:
            try:
                # Validate table name exists
                check_table = cursor.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                    (table_name,)
                ).fetchone()
                if not check_table:
                    continue
                    
                # Table name is validated, safe to use in query
                rows = cursor.execute(f"""
                    SELECT article_id, quantite
                    FROM {table_name}
                    WHERE inventaire_id=?
                """, (inventaire_id,)).fetchall()
                
                for row in rows:
                    snapshot.append({"article_id": row[0], "quantite": row[1]})
            except Exception as e:
                logger.warning(f"Could not query table {table_name}: {e}")
                continue

        if not snapshot:
            logger.warning(
                f"No inventory lines found for inventory {inventaire_id} "
                f"in tables {lines_table_candidates}"
            )
            return

        for item in snapshot:
            article_id = item.get("article_id")
            new_quantity = item.get("quantite", 0)

            # Get current stock
            current_stock = get_stock(conn, article_id)

            # Calculate delta
            delta = new_quantity - current_stock

            # Update stock
            set_stock(conn, article_id, new_quantity)

            # Record in journal
            cursor.execute("""
                INSERT INTO inventory_stock_journal
                (inventaire_id, article_id, delta, scope)
                VALUES (?, ?, ?, 'buvette')
            """, (inventaire_id, article_id, delta))

            logger.debug(
                f"Applied inventory snapshot for article {article_id}: "
                f"{current_stock} -> {new_quantity} (delta: {delta})"
            )

        logger.info(
            f"Applied inventory snapshot for inventory {inventaire_id} "
            f"with {len(snapshot)} items"
        )
    except Exception as e:
        logger.error(f"Error applying inventory snapshot for inventory {inventaire_id}: {e}")
        raise


def revert_inventory_effect(conn, inventaire_id):
    """
    Annule les effets d'un inventaire sur le stock en utilisant le journal.

    Args:
        conn: Database connection
        inventaire_id: ID de l'inventaire dont il faut annuler les effets

    Cette fonction:
    1. Récupère tous les deltas enregistrés pour cet inventaire
    2. Applique l'inverse de chaque delta au stock actuel
    3. Supprime les entrées du journal pour cet inventaire
    """
    try:
        cursor = conn.cursor()

        # Get all deltas for this inventory
        rows = cursor.execute("""
            SELECT article_id, delta FROM inventory_stock_journal
            WHERE inventaire_id=?
        """, (inventaire_id,)).fetchall()

        for row in rows:
            article_id = row[0]
            delta = row[1]

            # Revert the delta
            current_stock = get_stock(conn, article_id)
            new_stock = max(0, current_stock - delta)

            set_stock(conn, article_id, new_stock)
            logger.debug(
                f"Reverted stock for article {article_id}: "
                f"{current_stock} -> {new_stock} (delta: -{delta})"
            )

        # Delete journal entries for this inventory
        cursor.execute(
            "DELETE FROM inventory_stock_journal WHERE inventaire_id=?",
            (inventaire_id,)
        )

        logger.info(
            f"Reverted inventory effects for inventory {inventaire_id} "
            f"({len(rows)} items)"
        )
    except Exception as e:
        logger.error(f"Error reverting inventory effects for inventory {inventaire_id}: {e}")
        raise


def inventory_stock_journal(inv_id):
    """
    Récupère l'historique des modifications de stock pour un inventaire.

    Args:
        inv_id: ID de l'inventaire

    Returns:
        list: Liste de dicts avec article_id, delta, created_at
    """
    conn = None
    try:
        conn = get_connection()
        rows = conn.execute("""
            SELECT j.*, a.name as article_name
            FROM inventory_stock_journal j
            LEFT JOIN buvette_articles a ON j.article_id = a.id
            WHERE j.inventaire_id=?
            ORDER BY j.created_at
        """, (inv_id,)).fetchall()
        return rows_to_dicts(rows)
    except Exception as e:
        logger.error(f"Error getting stock journal for inventory {inv_id}: {e}")
        return []
    finally:
        if conn:
            conn.close()
