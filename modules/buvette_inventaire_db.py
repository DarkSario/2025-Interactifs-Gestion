"""
Module de gestion de la base de données pour les inventaires de la buvette.

STANDARDIZATION (PR copilot/audit-db-access-standardization):
- Improved connection management with try/finally blocks to reduce locks
- Converted sqlite3.Row to dicts for consistent .get() access patterns
- Added docstrings and error handling
"""

from db.db import get_connection
from utils.db_helpers import rows_to_dicts, row_to_dict
from utils.app_logger import get_logger
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

def delete_inventaire(inv_id):
    """Delete inventaire by ID."""
    conn = None
    try:
        conn = get_conn()
        conn.execute("DELETE FROM buvette_inventaires WHERE id=?", (inv_id,))
        conn.commit()
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