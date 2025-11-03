"""
Integration test for inventory service with legacy schema compatibility.

This test verifies that InventoryService works with both new and legacy
database schemas, ensuring backward compatibility.
"""

import pytest
from src.services.inventory_service import InventoryService
from src.db.connection import connect, transaction


def test_inventory_service_with_legacy_schema(tmp_path):
    """Test that InventoryService works with legacy buvette schema."""
    dbfile = tmp_path / "legacy.db"
    
    # Create legacy schema (buvette_inventaire_lignes with article_id and quantite)
    conn = connect(dbfile)
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS buvette_inventaires (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                created_at TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS buvette_inventaire_lignes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                inventaire_id INTEGER,
                article_id INTEGER,
                quantite INTEGER
            )
        """)
        # Insert test inventory
        conn.execute(
            "INSERT INTO buvette_inventaires (name, created_at) VALUES (?, datetime('now'))",
            ("Test Inventory",)
        )
        inv_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        
        # Insert test lines
        conn.execute(
            "INSERT INTO buvette_inventaire_lignes (inventaire_id, article_id, quantite) "
            "VALUES (?, ?, ?)",
            (inv_id, 101, 50)
        )
        conn.execute(
            "INSERT INTO buvette_inventaire_lignes (inventaire_id, article_id, quantite) "
            "VALUES (?, ?, ?)",
            (inv_id, 102, 30)
        )
    conn.close()
    
    # Use InventoryService to load lines
    service = InventoryService(dbfile)
    lines = service.load_inventory_lines(inv_id)
    
    # Verify schema detection and mapping worked
    assert len(lines) == 2
    
    # Check that columns are mapped correctly (article_id -> product_id, quantite -> qty)
    line1 = lines[0]
    assert 'product_id' in line1, "product_id should be mapped from article_id"
    assert 'qty' in line1, "qty should be mapped from quantite"
    assert line1['product_id'] == 101
    assert line1['qty'] == 50
    
    line2 = lines[1]
    assert line2['product_id'] == 102
    assert line2['qty'] == 30


def test_inventory_service_with_new_schema(tmp_path):
    """Test that InventoryService works with new schema."""
    dbfile = tmp_path / "new.db"
    
    # Create new schema (inventory_lines with product_id and qty)
    conn = connect(dbfile)
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS inventaires (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                created_at TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS inventory_lines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                inventaire_id INTEGER,
                product_id INTEGER,
                qty INTEGER
            )
        """)
        # Insert test inventory
        conn.execute(
            "INSERT INTO inventaires (name, created_at) VALUES (?, datetime('now'))",
            ("Test Inventory",)
        )
        inv_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        
        # Insert test lines
        conn.execute(
            "INSERT INTO inventory_lines (inventaire_id, product_id, qty) "
            "VALUES (?, ?, ?)",
            (inv_id, 201, 75)
        )
    conn.close()
    
    # Use InventoryService to load lines
    service = InventoryService(dbfile)
    lines = service.load_inventory_lines(inv_id)
    
    # Verify
    assert len(lines) == 1
    line = lines[0]
    assert line['product_id'] == 201
    assert line['qty'] == 75


def test_inventory_service_with_stock_schema(tmp_path):
    """Test that InventoryService works with stock-based schema."""
    dbfile = tmp_path / "stock.db"
    
    # Create stock schema (inventaire_lignes with stock_id and quantite_constatee)
    conn = connect(dbfile)
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS inventaires (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                created_at TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS inventaire_lignes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                inventaire_id INTEGER,
                stock_id INTEGER,
                quantite_constatee INTEGER
            )
        """)
        # Insert test inventory
        conn.execute(
            "INSERT INTO inventaires (name, created_at) VALUES (?, datetime('now'))",
            ("Test Inventory",)
        )
        inv_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        
        # Insert test lines
        conn.execute(
            "INSERT INTO inventaire_lignes (inventaire_id, stock_id, quantite_constatee) "
            "VALUES (?, ?, ?)",
            (inv_id, 301, 25)
        )
        conn.execute(
            "INSERT INTO inventaire_lignes (inventaire_id, stock_id, quantite_constatee) "
            "VALUES (?, ?, ?)",
            (inv_id, 302, 15)
        )
    conn.close()
    
    # Use InventoryService to load lines
    service = InventoryService(dbfile)
    lines = service.load_inventory_lines(inv_id)
    
    # Verify schema detection and mapping worked (stock_id -> product_id, quantite_constatee -> qty)
    assert len(lines) == 2
    
    line1 = lines[0]
    assert line1['product_id'] == 301
    assert line1['qty'] == 25
    
    line2 = lines[1]
    assert line2['product_id'] == 302
    assert line2['qty'] == 15


def test_inventory_service_empty_inventory(tmp_path):
    """Test that InventoryService handles empty inventories correctly."""
    dbfile = tmp_path / "empty.db"
    
    # Create schema with no lines
    conn = connect(dbfile)
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS inventaires (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                created_at TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS inventory_lines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                inventaire_id INTEGER,
                product_id INTEGER,
                qty INTEGER
            )
        """)
        # Insert test inventory with no lines
        conn.execute(
            "INSERT INTO inventaires (name, created_at) VALUES (?, datetime('now'))",
            ("Empty Inventory",)
        )
        inv_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.close()
    
    # Use InventoryService to load lines
    service = InventoryService(dbfile)
    lines = service.load_inventory_lines(inv_id)
    
    # Should return empty list, not error
    assert lines == []


def test_inventory_service_schema_caching(tmp_path):
    """Test that InventoryService caches schema detection for performance."""
    dbfile = tmp_path / "cached.db"
    
    # Create schema
    conn = connect(dbfile)
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS inventaires (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                created_at TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS inventory_lines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                inventaire_id INTEGER,
                product_id INTEGER,
                qty INTEGER
            )
        """)
        # Insert test inventory
        conn.execute(
            "INSERT INTO inventaires (name, created_at) VALUES (?, datetime('now'))",
            ("Test",)
        )
        inv_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        conn.execute(
            "INSERT INTO inventory_lines (inventaire_id, product_id, qty) "
            "VALUES (?, ?, ?)",
            (inv_id, 1, 10)
        )
    conn.close()
    
    # Create service and load lines twice
    service = InventoryService(dbfile)
    lines1 = service.load_inventory_lines(inv_id)
    
    # Schema should be cached
    assert service._schema_cache, "Schema should be cached after first load"
    
    # Load again
    lines2 = service.load_inventory_lines(inv_id)
    
    # Both loads should produce same results
    assert lines1 == lines2
    assert len(lines1) == 1
