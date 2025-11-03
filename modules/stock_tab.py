"""
Module UI helper pour l'affichage du stock.

Ce module fournit des fonctions utilitaires pour récupérer et formater
les données de stock pour l'interface utilisateur.
"""

from db.db import get_connection
from utils.db_helpers import rows_to_dicts
from utils.app_logger import get_logger

logger = get_logger("stock_tab")

# Cache for schema detection to avoid repeated PRAGMA queries
# Note: Cache is per-database-path to handle different test databases
_schema_cache = {}


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
    ALLOWED_TABLES = {'buvette_articles', 'stock', 'inventaire_lignes'}
    
    if table_name not in ALLOWED_TABLES:
        raise ValueError(f"Table '{table_name}' not in whitelist")
    
    cache_key = _get_cache_key(table_name)
    if cache_key not in _schema_cache:
        # Table name is validated against whitelist, safe to use in PRAGMA
        cursor = conn.execute(f"PRAGMA table_info({table_name})")
        _schema_cache[cache_key] = [row[1] for row in cursor.fetchall()]
    return _schema_cache[cache_key]


def clear_schema_cache():
    """Clear the schema cache. Useful for testing or after database migrations."""
    global _schema_cache
    _schema_cache = {}


def get_stock_listing(scope='buvette'):
    """
    Récupère la liste des articles avec leur stock pour l'UI.

    Args:
        scope: Filter by scope (default='buvette'). Currently only 'buvette' is supported.

    Returns:
        list: Liste de dicts avec les informations des articles et stock.
              Chaque dict: id, name, categorie, stock, quantite, unite_type,
              contenance, commentaire
              
              For backward compatibility, if 'unite' column exists (pre-migration),
              it will be returned. After migration, 'quantite' and 'unite_type' 
              columns will be returned instead.
    """
    conn = None
    try:
        conn = get_connection()
        # For now, we only support 'buvette' scope which maps to buvette_articles table
        # In the future, other scopes could be added (e.g., 'materiel' for stock table)
        if scope == 'buvette':
            # Check which columns exist for backward compatibility (cached for performance)
            columns = _get_table_columns(conn, 'buvette_articles')
            
            # Build SELECT clause based on available columns
            select_parts = ['id', 'name', 'categorie', 'stock']
            
            # Handle unite vs quantite/unite_type migration
            if 'quantite' in columns:
                select_parts.append('quantite')
            if 'unite_type' in columns:
                select_parts.append('unite_type')
            elif 'unite' in columns:
                # Legacy schema - provide compatibility
                select_parts.append('unite')
            
            select_parts.extend(['contenance', 'commentaire'])
            
            # Filter to only columns that exist
            select_parts = [col for col in select_parts if col in columns]
            
            # Whitelist of allowed column names for security
            ALLOWED_COLUMNS = {
                'id', 'name', 'categorie', 'stock', 'quantite',
                'unite_type', 'unite', 'contenance', 'commentaire'
            }
            
            # Validate all column names against whitelist
            for col in select_parts:
                if col not in ALLOWED_COLUMNS:
                    raise ValueError(f"Column '{col}' not in whitelist")
            
            select_clause = ', '.join(select_parts)
            # Column names are validated against whitelist, safe to use in query
            rows = conn.execute(f"""
                SELECT {select_clause}
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
