"""
Module de gestion de la base de données pour le module Buvette.

MODIFICATIONS APPLIQUÉES (PR corrections buvette - copilot/auto-fix-buvette):
- Harmonisation des noms de colonnes pour buvette_mouvements:
  * INSERT et UPDATE utilisent maintenant date_mouvement, type_mouvement, motif
    (au lieu de date, type, commentaire) pour correspondre au schéma DB
  * Les SELECT ajoutent des alias (AS date, AS type, AS commentaire) pour
    maintenir la compatibilité avec le code UI existant

- Ajout de la gestion du stock (PR copilot/auto-fix-buvette):
  * Fonction ensure_stock_column(): migration non destructive pour ajouter la colonne 'stock'
  * Fonction set_article_stock(article_id, stock): mise à jour du stock d'un article
  * Fonction get_article_stock(article_id): récupération du stock actuel d'un article
  * Ces fonctions permettent de suivre les quantités en stock après chaque inventaire

STANDARDIZATION (PR copilot/audit-db-access-standardization):
- Improved connection management with try/finally blocks to reduce locks
- Converted sqlite3.Row to dicts for consistent .get() access patterns
- Centralized error handling

TODO (audit/fixes-buvette):
- All functions normalized to return dicts via rows_to_dicts/row_to_dict
- Review reports/TODOs.md for additional audit findings
"""

from db.db import get_connection
from utils.db_helpers import rows_to_dicts, row_to_dict
from utils.app_logger import get_logger
from modules.stock_db import adjust_stock
import sqlite3

logger = get_logger("buvette_db")

# Cache for schema detection to avoid repeated PRAGMA queries
# Note: Cache is per-database-path to handle different test databases
_schema_cache = {}

def get_conn():
    conn = get_connection()
    return conn

def _get_cache_key(table_name):
    """Generate cache key based on database path and table name."""
    import os
    db_path = os.environ.get("APP_DB_PATH", "association.db")
    return f"{db_path}:{table_name}"

def _get_table_columns(conn, table_name):
    """
    Get column names for a table, with caching.
    
    Args:
        conn: Database connection
        table_name: Name of the table (validated against whitelist)
        
    Returns:
        list: Column names
    
    Raises:
        ValueError: If table_name is not in the whitelist
    """
    # Whitelist of allowed table names for security
    ALLOWED_TABLES = {'buvette_articles', 'buvette_achats', 'buvette_mouvements'}
    
    if table_name not in ALLOWED_TABLES:
        raise ValueError(f"Table '{table_name}' not in whitelist")
    
    cache_key = _get_cache_key(table_name)
    if cache_key not in _schema_cache:
        # Table name is validated against whitelist, safe to use in PRAGMA
        cursor = conn.execute(f"PRAGMA table_info({table_name})")
        _schema_cache[cache_key] = [row[1] for row in cursor.fetchall()]
    return _schema_cache[cache_key]

def _has_unite_type_schema(conn):
    """
    Check if database has post-migration schema (unite_type column).
    
    Args:
        conn: Database connection
        
    Returns:
        bool: True if post-migration schema, False if pre-migration
    """
    columns = _get_table_columns(conn, "buvette_articles")
    return 'unite_type' in columns

def clear_schema_cache():
    """Clear the schema cache. Useful for testing or after database migrations."""
    global _schema_cache
    _schema_cache = {}

# ----- ARTICLES -----
def list_articles():
    """List all articles, returns list of dicts for .get() access."""
    conn = None
    try:
        conn = get_conn()
        rows = conn.execute("SELECT * FROM buvette_articles ORDER BY name").fetchall()
        return rows_to_dicts(rows)
    finally:
        if conn:
            conn.close()

def get_article_by_id(article_id):
    """Get article by ID, returns dict or None."""
    conn = None
    try:
        conn = get_conn()
        row = conn.execute("SELECT * FROM buvette_articles WHERE id=?", (article_id,)).fetchone()
        return row_to_dict(row)
    finally:
        if conn:
            conn.close()

def insert_article(name, categorie, unite, commentaire, contenance, purchase_price=None):
    """
    Insert new article.
    
    Handles both pre-migration (unite) and post-migration (quantite, unite_type) schemas.
    The 'unite' parameter is used for backward compatibility:
    - Pre-migration: stored in 'unite' column
    - Post-migration: stored in 'unite_type' column
    """
    conn = None
    try:
        conn = get_conn()
        
        # Check which schema is in use (cached for performance)
        if _has_unite_type_schema(conn):
            # Post-migration schema: use unite_type instead of unite
            conn.execute("""
                INSERT INTO buvette_articles (name, categorie, unite_type, commentaire, contenance, purchase_price)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (name, categorie, unite, commentaire, contenance, purchase_price))
        else:
            # Pre-migration schema: use unite
            conn.execute("""
                INSERT INTO buvette_articles (name, categorie, unite, commentaire, contenance, purchase_price)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (name, categorie, unite, commentaire, contenance, purchase_price))
        
        conn.commit()
    finally:
        if conn:
            conn.close()

def update_article(article_id, name, categorie, unite, commentaire, contenance, purchase_price=None):
    """
    Update existing article.
    
    Handles both pre-migration (unite) and post-migration (quantite, unite_type) schemas.
    The 'unite' parameter is used for backward compatibility:
    - Pre-migration: updates 'unite' column
    - Post-migration: updates 'unite_type' column
    """
    conn = None
    try:
        conn = get_conn()
        
        # Check which schema is in use (cached for performance)
        if _has_unite_type_schema(conn):
            # Post-migration schema: use unite_type instead of unite
            conn.execute("""
                UPDATE buvette_articles SET name=?, categorie=?, unite_type=?, commentaire=?, contenance=?, purchase_price=?
                WHERE id=?
            """, (name, categorie, unite, commentaire, contenance, purchase_price, article_id))
        else:
            # Pre-migration schema: use unite
            conn.execute("""
                UPDATE buvette_articles SET name=?, categorie=?, unite=?, commentaire=?, contenance=?, purchase_price=?
                WHERE id=?
            """, (name, categorie, unite, commentaire, contenance, purchase_price, article_id))
        
        conn.commit()
    finally:
        if conn:
            conn.close()

def delete_article(article_id):
    """Delete article by ID."""
    conn = None
    try:
        conn = get_conn()
        conn.execute("DELETE FROM buvette_articles WHERE id=?", (article_id,))
        conn.commit()
    finally:
        if conn:
            conn.close()

# ----- ACHATS -----
def list_achats():
    """List all achats with article info, returns list of dicts."""
    conn = None
    try:
        conn = get_conn()
        rows = conn.execute("""
            SELECT a.*, ar.name AS article_name, ar.contenance AS article_contenance
            FROM buvette_achats a
            LEFT JOIN buvette_articles ar ON a.article_id = ar.id
            ORDER BY a.date_achat DESC
        """).fetchall()
        return rows_to_dicts(rows)
    finally:
        if conn:
            conn.close()

def get_achat_by_id(achat_id):
    """Get achat by ID with article info, returns dict or None."""
    conn = None
    try:
        conn = get_conn()
        row = conn.execute("""
            SELECT a.*, ar.name AS article_name, ar.contenance AS article_contenance
            FROM buvette_achats a
            LEFT JOIN buvette_articles ar ON a.article_id = ar.id
            WHERE a.id=?
        """, (achat_id,)).fetchone()
        return row_to_dict(row)
    finally:
        if conn:
            conn.close()

def insert_achat(article_id, date_achat, quantite, prix_unitaire, fournisseur, facture, exercice):
    """
    Insert new achat, adjust stock, and update purchase_price.
    
    TODO (audit/fixes-buvette): Review price update strategy.
    Current: purchase_price = latest prix_unitaire from achat
    Alternatives: weighted average, FIFO-based price, keep highest/lowest
    Decision needed: should purchase_price reflect latest or average cost?
    See reports/TODOs.md for pricing strategy review.
    """
    conn = None
    try:
        conn = get_conn()
        conn.execute("""
            INSERT INTO buvette_achats (article_id, date_achat, quantite, prix_unitaire, fournisseur, facture, exercice)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (article_id, date_achat, quantite, prix_unitaire, fournisseur, facture, exercice))
        
        # Update article's purchase_price if prix_unitaire is provided
        if prix_unitaire is not None:
            try:
                conn.execute("""
                    UPDATE buvette_articles 
                    SET purchase_price = ? 
                    WHERE id = ?
                """, (prix_unitaire, article_id))
                logger.info(f"Updated purchase_price for article {article_id} to {prix_unitaire}")
            except Exception as e:
                logger.warning(f"Could not update purchase_price for article {article_id}: {e}")
        
        conn.commit()
        
        # Adjust stock: add purchased quantity
        try:
            adjust_stock(article_id, quantite, reason=f"Achat: facture {facture}")
            logger.info(f"Adjusted stock for article {article_id} by +{quantite} (purchase)")
        except Exception as e:
            logger.warning(f"Could not adjust stock after purchase: {e}")
    finally:
        if conn:
            conn.close()

def update_achat(achat_id, article_id, date_achat, quantite, prix_unitaire, fournisseur, facture, exercice):
    """
    Update existing achat and update purchase_price if changed.
    
    TODO (audit/fixes-buvette): Review if price should update on achat modification.
    Current: Updates purchase_price when achat is modified
    Concern: May overwrite more recent purchase prices with older data
    Consider: Only update if this achat date_achat is the most recent
    See reports/TODOs.md for pricing strategy review.
    """
    conn = None
    try:
        conn = get_conn()
        conn.execute("""
            UPDATE buvette_achats SET article_id=?, date_achat=?, quantite=?, prix_unitaire=?,
                fournisseur=?, facture=?, exercice=?
            WHERE id=?
        """, (article_id, date_achat, quantite, prix_unitaire, fournisseur, facture, exercice, achat_id))
        
        # Update article's purchase_price if prix_unitaire is provided
        if prix_unitaire is not None:
            try:
                conn.execute("""
                    UPDATE buvette_articles 
                    SET purchase_price = ? 
                    WHERE id = ?
                """, (prix_unitaire, article_id))
                logger.info(f"Updated purchase_price for article {article_id} to {prix_unitaire}")
            except Exception as e:
                logger.warning(f"Could not update purchase_price for article {article_id}: {e}")
        
        conn.commit()
    finally:
        if conn:
            conn.close()

def delete_achat(achat_id):
    """Delete achat by ID and revert stock adjustment."""
    conn = None
    try:
        conn = get_conn()
        
        # Get achat details before deletion to revert stock
        row = conn.execute(
            "SELECT article_id, quantite FROM buvette_achats WHERE id=?",
            (achat_id,)
        ).fetchone()
        
        if row:
            article_id = row[0]
            quantite = row[1]
            
            # Delete the achat
            conn.execute("DELETE FROM buvette_achats WHERE id=?", (achat_id,))
            conn.commit()
            
            # Revert stock: subtract the purchased quantity
            try:
                adjust_stock(article_id, -quantite, reason=f"Suppression achat #{achat_id}")
                logger.info(f"Adjusted stock for article {article_id} by -{quantite} (delete purchase)")
            except Exception as e:
                logger.warning(f"Could not revert stock after deleting purchase: {e}")
    finally:
        if conn:
            conn.close()

# ----- MOUVEMENTS -----
def list_mouvements():
    """List all mouvements with article info, returns list of dicts."""
    conn = None
    try:
        conn = get_conn()
        rows = conn.execute("""
            SELECT m.*, 
                   m.date_mouvement AS date, 
                   m.type_mouvement AS type,
                   m.motif AS commentaire,
                   ar.name AS article_name, 
                   ar.contenance AS article_contenance
            FROM buvette_mouvements m
            LEFT JOIN buvette_articles ar ON m.article_id = ar.id
            ORDER BY m.date_mouvement DESC
        """).fetchall()
        return rows_to_dicts(rows)
    finally:
        if conn:
            conn.close()

def get_mouvement_by_id(mvt_id):
    """Get mouvement by ID with article info, returns dict or None."""
    conn = None
    try:
        conn = get_conn()
        row = conn.execute("""
            SELECT m.*, 
                   m.date_mouvement AS date, 
                   m.type_mouvement AS type,
                   m.motif AS commentaire,
                   ar.name AS article_name, 
                   ar.contenance AS article_contenance
            FROM buvette_mouvements m
            LEFT JOIN buvette_articles ar ON m.article_id = ar.id
            WHERE m.id=?
        """, (mvt_id,)).fetchone()
        return row_to_dict(row)
    finally:
        if conn:
            conn.close()

def insert_mouvement(date_mouvement, article_id, type_mouvement, quantite, motif):
    """Insert new mouvement."""
    conn = None
    try:
        conn = get_conn()
        conn.execute("""
            INSERT INTO buvette_mouvements (date_mouvement, article_id, type_mouvement, quantite, motif)
            VALUES (?, ?, ?, ?, ?)
        """, (date_mouvement, article_id, type_mouvement, quantite, motif))
        conn.commit()
    finally:
        if conn:
            conn.close()

def update_mouvement(mvt_id, date_mouvement, article_id, type_mouvement, quantite, motif):
    """Update existing mouvement."""
    conn = None
    try:
        conn = get_conn()
        conn.execute("""
            UPDATE buvette_mouvements SET date_mouvement=?, article_id=?, type_mouvement=?, quantite=?, motif=?
            WHERE id=?
        """, (date_mouvement, article_id, type_mouvement, quantite, motif, mvt_id))
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

# ----- INVENTAIRE LIGNES -----
def list_lignes_inventaire(inventaire_id):
    """List inventory lines for a specific inventory, returns list of dicts."""
    conn = None
    try:
        conn = get_conn()
        rows = conn.execute("""
            SELECT l.*, ar.name AS article_name, ar.contenance AS article_contenance
            FROM buvette_inventaire_lignes l
            LEFT JOIN buvette_articles ar ON l.article_id = ar.id
            WHERE l.inventaire_id=?
            ORDER BY l.id
        """, (inventaire_id,)).fetchall()
        return rows_to_dicts(rows)
    finally:
        if conn:
            conn.close()

def insert_ligne_inventaire(inventaire_id, article_id, quantite, commentaire):
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

def update_ligne_inventaire(ligne_id, article_id, quantite, commentaire):
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

# ----- UTILITY -----
def list_articles_names():
    """List article IDs, names and contenance, returns list of dicts."""
    conn = None
    try:
        conn = get_conn()
        rows = conn.execute("SELECT id, name, contenance FROM buvette_articles ORDER BY name").fetchall()
        return rows_to_dicts(rows)
    finally:
        if conn:
            conn.close()

def ensure_stock_column():
    """
    Migration non destructive: Ajoute la colonne 'stock' à buvette_articles si elle n'existe pas.
    Cette fonction doit être appelée au démarrage de l'application ou lors de la mise à jour de la DB.
    """
    conn = None
    try:
        conn = get_conn()
        # Vérifier si la colonne stock existe déjà
        cursor = conn.execute("PRAGMA table_info(buvette_articles)")
        columns = [row["name"] for row in cursor.fetchall()]
        
        if "stock" not in columns:
            conn.execute("ALTER TABLE buvette_articles ADD COLUMN stock INTEGER DEFAULT 0")
            conn.commit()
            logger.info("Column 'stock' added to buvette_articles")
            return True  # Colonne ajoutée
        return False  # Colonne existait déjà
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Error ensuring stock column: {e}")
        raise e
    finally:
        if conn:
            conn.close()

def set_article_stock(article_id, stock):
    """
    Met à jour le stock d'un article.
    Cette fonction est appelée après l'enregistrement d'un inventaire pour mettre à jour
    le stock de l'article immédiatement.
    
    Args:
        article_id: ID de l'article
        stock: Nouvelle valeur du stock (quantité en unités)
    """
    conn = None
    try:
        conn = get_conn()
        conn.execute("UPDATE buvette_articles SET stock=? WHERE id=?", (stock, article_id))
        conn.commit()
    finally:
        if conn:
            conn.close()

def get_article_stock(article_id):
    """
    Récupère le stock actuel d'un article.
    
    Args:
        article_id: ID de l'article
        
    Returns:
        int: Stock actuel de l'article (0 si la colonne n'existe pas ou si l'article n'existe pas)
    """
    conn = None
    try:
        conn = get_conn()
        # Vérifier si la colonne stock existe
        cursor = conn.execute("PRAGMA table_info(buvette_articles)")
        columns = [row["name"] for row in cursor.fetchall()]
        
        if "stock" in columns:
            row = conn.execute("SELECT stock FROM buvette_articles WHERE id=?", (article_id,)).fetchone()
            return row_to_dict(row).get("stock", 0) if row else 0
        else:
            return 0
    finally:
        if conn:
            conn.close()