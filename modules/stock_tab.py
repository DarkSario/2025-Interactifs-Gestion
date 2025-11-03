"""
Module UI helper pour l'affichage du stock.

Ce module fournit des fonctions utilitaires pour récupérer et formater
les données de stock pour l'affichage dans l'interface utilisateur.
"""

from db.db import get_connection
from utils.db_helpers import rows_to_dicts
from utils.app_logger import get_logger

logger = get_logger("stock_tab")


def get_stock_listing(scope='buvette'):
    """
    Récupère la liste des articles avec leur stock pour l'UI.

    Args:
        scope: Filter by scope (default='buvette'). Currently only 'buvette' is supported.

    Returns:
        list: Liste de dicts avec les informations des articles et stock.
              Chaque dict: id, name, categorie, stock, unite, contenance,
              commentaire
    """
    conn = None
    try:
        conn = get_connection()
        # For now, we only support 'buvette' scope which maps to buvette_articles table
        # In the future, other scopes could be added (e.g., 'materiel' for stock table)
        if scope == 'buvette':
            rows = conn.execute("""
                SELECT id, name, categorie, stock, unite, contenance, commentaire
                FROM buvette_articles
                ORDER BY name
            """).fetchall()
        else:
            logger.warning(f"Unsupported scope: {scope}, returning empty list")
            rows = []
        return rows_to_dicts(rows)
    except Exception as e:
        logger.error(f"Error getting stock listing for scope {scope}: {e}")
        return []
    finally:
        if conn:
            conn.close()
