"""
Module de gestion de la base de données pour les mouvements de stock de la buvette.

STANDARDIZATION (PR copilot/audit-db-access-standardization):
- Improved connection management with try/finally blocks to reduce locks
- Converted sqlite3.Row to dicts for consistent .get() access patterns
- Added docstrings and error handling

TODO (audit/fixes-buvette): 
- Added SELECT aliases for UI compatibility (date_mouvement AS date, etc.)
- Review reports/TODOs.md for additional changes
"""

from db.db import get_connection
from utils.db_helpers import rows_to_dicts, row_to_dict
from utils.app_logger import get_logger
import sqlite3

logger = get_logger("buvette_mouvements_db")

def get_conn():
    conn = get_connection()
    return conn

# ----- MOUVEMENTS -----
def list_mouvements():
    """List all mouvements with article and event info, returns list of dicts.
    
    TODO (audit/fixes-buvette): Added aliases for UI compatibility
    - m.date_mouvement AS date
    - m.type_mouvement AS type  
    - m.motif AS commentaire
    """
    conn = None
    try:
        conn = get_conn()
        rows = conn.execute("""
            SELECT m.id, m.article_id, m.quantite, m.event_id,
                   m.date_mouvement AS date, 
                   m.type_mouvement AS type, 
                   m.motif AS commentaire,
                   a.name AS article_name, 
                   e.name AS event_name, 
                   e.date AS event_date
            FROM buvette_mouvements m
            LEFT JOIN buvette_articles a ON m.article_id = a.id
            LEFT JOIN events e ON m.event_id = e.id
            ORDER BY m.date_mouvement DESC
        """).fetchall()
        return rows_to_dicts(rows)
    finally:
        if conn:
            conn.close()

def get_mouvement_by_id(mvt_id):
    """Get mouvement by ID with article and event info, returns dict or None.
    
    TODO (audit/fixes-buvette): Added aliases for UI compatibility
    """
    conn = None
    try:
        conn = get_conn()
        row = conn.execute("""
            SELECT m.id, m.article_id, m.quantite, m.event_id,
                   m.date_mouvement AS date, 
                   m.type_mouvement AS type, 
                   m.motif AS commentaire,
                   a.name AS article_name, 
                   e.name AS event_name, 
                   e.date AS event_date
            FROM buvette_mouvements m
            LEFT JOIN buvette_articles a ON m.article_id = a.id
            LEFT JOIN events e ON m.event_id = e.id
            WHERE m.id=?
        """, (mvt_id,)).fetchone()
        return row_to_dict(row)
    finally:
        if conn:
            conn.close()

def insert_mouvement(article_id, date_mouvement, type_mouvement, quantite, motif, event_id):
    """Insert new mouvement."""
    conn = None
    try:
        conn = get_conn()
        conn.execute("""
            INSERT INTO buvette_mouvements (article_id, date_mouvement, type_mouvement, quantite, motif, event_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (article_id, date_mouvement, type_mouvement, quantite, motif, event_id))
        conn.commit()
    finally:
        if conn:
            conn.close()

def update_mouvement(mvt_id, article_id, date_mouvement, type_mouvement, quantite, motif, event_id):
    """Update existing mouvement."""
    conn = None
    try:
        conn = get_conn()
        conn.execute("""
            UPDATE buvette_mouvements SET article_id=?, date_mouvement=?, type_mouvement=?, quantite=?, motif=?, event_id=?
            WHERE id=?
        """, (article_id, date_mouvement, type_mouvement, quantite, motif, event_id, mvt_id))
        conn.commit()
    finally:
        if conn:
            conn.close()

def delete_mouvement(mvt_id):
    """Delete mouvement by ID."""
    conn = None
    try:
        conn = get_conn()
        conn.execute("DELETE FROM buvette_mouvements WHERE id=?", (mvt_id,))
        conn.commit()
    finally:
        if conn:
            conn.close()

# ----- UTILITY -----
def list_articles():
    """List articles for dropdown, returns list of dicts."""
    conn = None
    try:
        conn = get_conn()
        rows = conn.execute("SELECT id, name FROM buvette_articles ORDER BY name").fetchall()
        return rows_to_dicts(rows)
    finally:
        if conn:
            conn.close()

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