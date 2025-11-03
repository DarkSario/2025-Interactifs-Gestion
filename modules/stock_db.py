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
- create_purchase_batch(): enregistre un lot d'achat avec prix unitaire
- consume_purchase_batches_fifo(): consomme des lots en FIFO pour calculer le coût

Toutes les opérations sont transactionnelles.
"""

from db.db import get_connection
from utils.db_helpers import rows_to_dicts
from utils.app_logger import get_logger

logger = get_logger("stock_db")


def ensure_stock_tables(conn=None):
    """
    Crée les tables nécessaires pour le journal de stock et les lots d'achat.
    
    Args:
        conn: Optional database connection. If None, creates a new connection.
    """
    conn_provided = conn is not None
    if not conn_provided:
        conn = get_connection()
    
    try:
        # Create inventory stock journal table
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
        
        # Create article purchase batches table for FIFO costing
        conn.execute("""
            CREATE TABLE IF NOT EXISTS article_purchase_batches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                article_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                remaining_quantity INTEGER NOT NULL,
                unit_price REAL NOT NULL,
                purchase_date TEXT DEFAULT CURRENT_TIMESTAMP,
                achat_id INTEGER,
                scope TEXT DEFAULT 'buvette',
                FOREIGN KEY (article_id) REFERENCES buvette_articles(id)
            )
        """)
        
        if not conn_provided:
            conn.commit()
        logger.info("Stock tables created/verified (inventory_stock_journal, article_purchase_batches)")
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
    # Whitelist of allowed table names for security
    ALLOWED_TABLES = {
        'buvette_inventaire_lignes': True,
        'inventaire_lignes': True,
    }
    
    if lines_table_candidates is None:
        lines_table_candidates = ['buvette_inventaire_lignes']
    
    try:
        cursor = conn.cursor()
        
        # Find inventory lines from candidate tables
        snapshot = []
        for table_name in lines_table_candidates:
            # Validate table name against whitelist
            if table_name not in ALLOWED_TABLES:
                logger.warning(
                    f"Table '{table_name}' not in whitelist, skipping"
                )
                continue
            
            try:
                # Verify table exists in database
                check_table = cursor.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                    (table_name,)
                ).fetchone()
                if not check_table:
                    continue
                    
                # Table name is validated against whitelist and confirmed to exist
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


def inventory_stock_journal(conn, inv_id):
    """
    Récupère l'historique des modifications de stock pour un inventaire.

    Args:
        conn: Database connection
        inv_id: ID de l'inventaire

    Returns:
        list: Liste de dicts avec article_id, delta, created_at
    """
    try:
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


def create_purchase_batch(conn, article_id, quantity, unit_price, achat_id=None, scope='buvette'):
    """
    Enregistre un lot d'achat avec prix unitaire pour le calcul FIFO.
    
    Args:
        conn: Database connection
        article_id: ID de l'article
        quantity: Quantité achetée
        unit_price: Prix unitaire du lot
        achat_id: ID de l'achat (optionnel, pour traçabilité)
        scope: Portée du stock (default='buvette')
    
    Returns:
        int: ID du lot créé
    """
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO article_purchase_batches
            (article_id, quantity, remaining_quantity, unit_price, achat_id, scope)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (article_id, quantity, quantity, unit_price, achat_id, scope))
        
        batch_id = cursor.lastrowid
        logger.info(
            f"Created purchase batch {batch_id} for article {article_id}: "
            f"qty={quantity}, unit_price={unit_price}"
        )
        return batch_id
    except Exception as e:
        logger.error(
            f"Error creating purchase batch for article {article_id}: {e}"
        )
        raise


def consume_purchase_batches_fifo(conn, article_id, consume_quantity, scope='buvette'):
    """
    Consomme des lots d'achat en FIFO et calcule le coût total.
    
    Args:
        conn: Database connection
        article_id: ID de l'article
        consume_quantity: Quantité à consommer
        scope: Portée du stock (default='buvette')
    
    Returns:
        dict: {
            'total_cost': coût total de la consommation,
            'consumed_batches': liste des lots consommés avec détails
        }
    """
    try:
        cursor = conn.cursor()
        
        # Get available batches in FIFO order (oldest first)
        rows = cursor.execute("""
            SELECT id, remaining_quantity, unit_price
            FROM article_purchase_batches
            WHERE article_id = ? AND scope = ? AND remaining_quantity > 0
            ORDER BY purchase_date ASC, id ASC
        """, (article_id, scope)).fetchall()
        
        total_cost = 0.0
        consumed_batches = []
        remaining_to_consume = consume_quantity
        
        for row in rows:
            if remaining_to_consume <= 0:
                break
                
            batch_id = row[0]
            batch_remaining = row[1]
            batch_unit_price = row[2]
            
            # Consume from this batch
            consumed_from_batch = min(remaining_to_consume, batch_remaining)
            cost_from_batch = consumed_from_batch * batch_unit_price
            
            # Update batch remaining quantity
            new_remaining = batch_remaining - consumed_from_batch
            cursor.execute("""
                UPDATE article_purchase_batches
                SET remaining_quantity = ?
                WHERE id = ?
            """, (new_remaining, batch_id))
            
            # Track this consumption
            consumed_batches.append({
                'batch_id': batch_id,
                'consumed_quantity': consumed_from_batch,
                'unit_price': batch_unit_price,
                'cost': cost_from_batch
            })
            
            total_cost += cost_from_batch
            remaining_to_consume -= consumed_from_batch
            
            logger.debug(
                f"Consumed {consumed_from_batch} from batch {batch_id} "
                f"at unit_price={batch_unit_price}, cost={cost_from_batch}"
            )
        
        if remaining_to_consume > 0:
            logger.warning(
                f"Could not fully consume {consume_quantity} units of article {article_id}. "
                f"Missing {remaining_to_consume} units from purchase batches. "
                f"Using average cost estimation for missing quantity."
            )
            # For missing quantity, use average of consumed batches or 0
            if consumed_batches:
                avg_price = total_cost / (consume_quantity - remaining_to_consume)
                additional_cost = remaining_to_consume * avg_price
                total_cost += additional_cost
                logger.warning(f"Estimated cost for missing quantity: {additional_cost}")
        
        logger.info(
            f"Consumed {consume_quantity} units of article {article_id} "
            f"via FIFO: total_cost={total_cost:.2f}, "
            f"batches_used={len(consumed_batches)}"
        )
        
        return {
            'total_cost': total_cost,
            'consumed_batches': consumed_batches
        }
    except Exception as e:
        logger.error(
            f"Error consuming purchase batches for article {article_id}: {e}"
        )
        raise


def recompute_stock_for_article(conn, article_id):
    """
    Recalcule le stock d'un article en agrégeant tous les mouvements signés.
    
    Cette fonction recalcule le stock à partir de zéro en sommant tous les
    mouvements de type 'entrée' (positifs) et 'sortie' (négatifs).
    
    Args:
        conn: Database connection
        article_id: ID de l'article
    
    Returns:
        int: Le nouveau stock calculé
        
    Note:
        - Les mouvements de type 'entrée' sont comptés positivement
        - Les mouvements de type 'sortie' sont comptés négativement
        - Le stock ne peut pas être négatif (minimum 0)
        - Cette fonction met à jour la colonne stock dans buvette_articles
        
    TODO (audit/fixes-buvette): 
        Voir reports/TODOs.md pour revue des types de mouvements supportés
    """
    try:
        cursor = conn.cursor()
        
        # Get all movements for this article
        # type_mouvement can be: 'entrée', 'sortie', 'inventaire', etc.
        rows = cursor.execute("""
            SELECT type_mouvement, quantite
            FROM buvette_mouvements
            WHERE article_id = ?
            ORDER BY date_mouvement ASC, id ASC
        """, (article_id,)).fetchall()
        
        calculated_stock = 0
        
        for row in rows:
            type_mouvement = row[0]
            quantite = row[1] if row[1] is not None else 0
            
            # Map movement types to signed quantities
            # 'entrée' and 'inventaire' add to stock
            # 'sortie' reduces stock
            if type_mouvement in ('entrée', 'inventaire', 'achat'):
                calculated_stock += quantite
            elif type_mouvement == 'sortie':
                calculated_stock -= quantite
            else:
                # Unknown type - log warning but don't fail
                logger.warning(
                    f"Unknown movement type '{type_mouvement}' for article {article_id}, "
                    f"treating as neutral (quantity: {quantite})"
                )
        
        # Stock cannot be negative
        calculated_stock = max(0, calculated_stock)
        
        # Update the article's stock
        set_stock(conn, article_id, calculated_stock)
        
        logger.info(
            f"Recomputed stock for article {article_id}: "
            f"{len(rows)} movements processed, final stock = {calculated_stock}"
        )
        
        return calculated_stock
        
    except Exception as e:
        logger.error(
            f"Error recomputing stock for article {article_id}: {e}"
        )
        raise
