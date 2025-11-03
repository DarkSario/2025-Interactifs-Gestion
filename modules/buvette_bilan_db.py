"""
Module de gestion de la base de données pour les bilans de la buvette.

STANDARDIZATION (PR copilot/audit-db-access-standardization):
- Improved connection management with try/finally blocks to reduce locks
- Converted sqlite3.Row to dicts for consistent .get() access patterns
- Added docstrings and error handling

TODO (audit/fixes-buvette):
- All functions normalized to return dicts via rows_to_dicts/row_to_dict
- Review reports/TODOs.md for additional audit findings
"""

from db.db import get_connection
from utils.db_helpers import rows_to_dicts, row_to_dict
from utils.app_logger import get_logger
import sqlite3

logger = get_logger("buvette_bilan_db")

def get_conn():
    conn = get_connection()
    return conn

def list_evenements():
    """Liste tous les événements pour lesquels il existe des inventaires buvette, returns list of dicts."""
    conn = None
    try:
        conn = get_conn()
        rows = conn.execute("SELECT id, name, date FROM events ORDER BY date DESC").fetchall()
        return rows_to_dicts(rows)
    finally:
        if conn:
            conn.close()

def get_inventaire_par_evenement(event_id, typ):
    """
    Récupère l'inventaire 'avant' ou 'après' pour un événement, returns dict or None.
    typ = 'avant' ou 'apres'
    """
    conn = None
    try:
        conn = get_conn()
        inv = conn.execute("""
            SELECT * FROM buvette_inventaires
            WHERE event_id=? AND type_inventaire=?
            ORDER BY date_inventaire ASC
            LIMIT 1
        """, (event_id, typ)).fetchone()
        return row_to_dict(inv)
    finally:
        if conn:
            conn.close()

def get_lignes_inventaire(inv_id):
    """
    Récupère les lignes d'inventaire (avec info article) pour un inventaire donné, returns list of dicts.
    """
    conn = None
    try:
        conn = get_conn()
        rows = conn.execute("""
            SELECT l.*, a.name as article_name, a.categorie, a.unite
            FROM buvette_inventaire_lignes l
            LEFT JOIN buvette_articles a ON l.article_id = a.id
            WHERE l.inventaire_id=?
            ORDER BY a.name
        """, (inv_id,)).fetchall()
        return rows_to_dicts(rows)
    finally:
        if conn:
            conn.close()

def get_prix_moyen_achat(article_id, jusqua_date=None):
    """
    Calcule le prix moyen pondéré d'achat d'un article jusqu'à une date donnée.
    Returns float.
    """
    conn = None
    try:
        conn = get_conn()
        q = "SELECT SUM(quantite*prix_unitaire) as total, SUM(quantite) as qte FROM buvette_achats WHERE article_id=?"
        params = [article_id]
        if jusqua_date:
            q += " AND date_achat<=?"
            params.append(jusqua_date)
        row = conn.execute(q, params).fetchone()
        row_dict = row_to_dict(row)
        if row_dict and row_dict.get("qte"):
            return row_dict["total"] / row_dict["qte"]
        return 0.0
    finally:
        if conn:
            conn.close()

def get_recette_buvette(event_id):
    """
    Récupère la somme totale des recettes buvette pour un événement.
    Returns float.
    """
    conn = None
    try:
        conn = get_conn()
        row = conn.execute("""
            SELECT SUM(montant) as recette
            FROM buvette_recettes
            WHERE event_id=?
        """, (event_id,)).fetchone()
        row_dict = row_to_dict(row)
        return row_dict.get("recette", 0.0) if row_dict else 0.0
    finally:
        if conn:
            conn.close()