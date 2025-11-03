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


def ensure_stock_tables():
    """
    Crée la table inventory_stock_journal si elle n'existe pas.
    Cette table enregistre les modifications de stock liées aux inventaires.
    """
    conn = None
    try:
        conn = get_connection()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS inventory_stock_journal (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                inventaire_id INTEGER NOT NULL,
                article_id INTEGER NOT NULL,
                delta INTEGER NOT NULL,
                date_created TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (inventaire_id) REFERENCES buvette_inventaires(id),
                FOREIGN KEY (article_id) REFERENCES buvette_articles(id)
            )
        """)
        conn.commit()
        logger.info("inventory_stock_journal table created/verified")
    except Exception as e:
        logger.error(f"Error ensuring stock tables: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()


def get_stock(article_id):
    """
    Récupère le stock actuel d'un article.

    Args:
        article_id: ID de l'article

    Returns:
        int: Stock actuel (0 si l'article n'existe pas ou n'a pas de stock)
    """
    conn = None
    try:
        conn = get_connection()
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
    finally:
        if conn:
            conn.close()


def set_stock(article_id, quantity):
    """
    Met à jour le stock d'un article à une valeur absolue.

    Args:
        article_id: ID de l'article
        quantity: Nouvelle quantité en stock
    """
    conn = None
    try:
        conn = get_connection()
        conn.execute(
            "UPDATE buvette_articles SET stock=? WHERE id=?",
            (quantity, article_id)
        )
        conn.commit()
        logger.debug(f"Set stock for article {article_id} to {quantity}")
    except Exception as e:
        logger.error(f"Error setting stock for article {article_id}: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()


def adjust_stock(article_id, delta, reason=None):
    """
    Ajuste le stock d'un article par un delta (positif ou négatif).

    Args:
        article_id: ID de l'article
        delta: Quantité à ajouter (positif) ou retirer (négatif)
        reason: Motif de l'ajustement (optionnel)
    """
    try:
        current_stock = get_stock(article_id)
        new_stock = max(0, current_stock + delta)
        set_stock(article_id, new_stock)
        logger.info(
            f"Adjusted stock for article {article_id} by {delta} "
            f"(reason: {reason})"
        )
    except Exception as e:
        logger.error(f"Error adjusting stock for article {article_id}: {e}")
        raise


def apply_inventory_snapshot(inv_id, snapshot):
    """
    Applique un snapshot d'inventaire et enregistre les deltas.

    Args:
        inv_id: ID de l'inventaire
        snapshot: Liste de dicts avec keys 'article_id' et 'quantite'

    Cette fonction:
    1. Calcule le delta entre le stock actuel et la quantité inventoriée
    2. Met à jour le stock de chaque article
    3. Enregistre les deltas dans inventory_stock_journal pour annulation
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("BEGIN")

        for item in snapshot:
            article_id = item.get("article_id")
            new_quantity = item.get("quantite", 0)

            # Get current stock
            row = cursor.execute(
                "SELECT stock FROM buvette_articles WHERE id=?",
                (article_id,)
            ).fetchone()
            current_stock = row[0] if row else 0

            # Calculate delta
            delta = new_quantity - current_stock

            # Update stock
            cursor.execute(
                "UPDATE buvette_articles SET stock=? WHERE id=?",
                (new_quantity, article_id)
            )

            # Record in journal
            cursor.execute("""
                INSERT INTO inventory_stock_journal
                (inventaire_id, article_id, delta)
                VALUES (?, ?, ?)
            """, (inv_id, article_id, delta))

            logger.debug(
                f"Applied inventory snapshot for article {article_id}: "
                f"{current_stock} -> {new_quantity} (delta: {delta})"
            )

        conn.commit()
        logger.info(
            f"Applied inventory snapshot for inventory {inv_id} "
            f"with {len(snapshot)} items"
        )
    except Exception as e:
        logger.error(f"Error applying inventory snapshot for inventory {inv_id}: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()


def revert_inventory_effect(inv_id):
    """
    Annule les effets d'un inventaire sur le stock en utilisant le journal.

    Args:
        inv_id: ID de l'inventaire dont il faut annuler les effets

    Cette fonction:
    1. Récupère tous les deltas enregistrés pour cet inventaire
    2. Applique l'inverse de chaque delta au stock actuel
    3. Supprime les entrées du journal pour cet inventaire
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("BEGIN")

        # Get all deltas for this inventory
        rows = cursor.execute("""
            SELECT article_id, delta FROM inventory_stock_journal
            WHERE inventaire_id=?
        """, (inv_id,)).fetchall()

        for row in rows:
            article_id = row[0]
            delta = row[1]

            # Revert the delta
            current_row = cursor.execute(
                "SELECT stock FROM buvette_articles WHERE id=?",
                (article_id,)
            ).fetchone()
            current_stock = current_row[0] if current_row else 0
            new_stock = max(0, current_stock - delta)

            cursor.execute(
                "UPDATE buvette_articles SET stock=? WHERE id=?",
                (new_stock, article_id)
            )
            logger.debug(
                f"Reverted stock for article {article_id}: "
                f"{current_stock} -> {new_stock} (delta: -{delta})"
            )

        # Delete journal entries for this inventory
        cursor.execute(
            "DELETE FROM inventory_stock_journal WHERE inventaire_id=?",
            (inv_id,)
        )

        conn.commit()
        logger.info(
            f"Reverted inventory effects for inventory {inv_id} "
            f"({len(rows)} items)"
        )
    except Exception as e:
        logger.error(f"Error reverting inventory effects for inventory {inv_id}: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()


def inventory_stock_journal(inv_id):
    """
    Récupère l'historique des modifications de stock pour un inventaire.

    Args:
        inv_id: ID de l'inventaire

    Returns:
        list: Liste de dicts avec article_id, delta, date_created
    """
    conn = None
    try:
        conn = get_connection()
        rows = conn.execute("""
            SELECT j.*, a.name as article_name
            FROM inventory_stock_journal j
            LEFT JOIN buvette_articles a ON j.article_id = a.id
            WHERE j.inventaire_id=?
            ORDER BY j.date_created
        """, (inv_id,)).fetchall()
        return rows_to_dicts(rows)
    except Exception as e:
        logger.error(f"Error getting stock journal for inventory {inv_id}: {e}")
        return []
    finally:
        if conn:
            conn.close()
