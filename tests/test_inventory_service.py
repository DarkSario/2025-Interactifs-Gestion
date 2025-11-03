from src.services.inventory_service import InventoryService
from src.db.connection import connect


def test_inventory_load_and_create(tmp_path):
    dbfile = tmp_path / "inv.db"
    conn = connect(dbfile)
    with conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS inventaires "
            "(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, "
            "created_at TEXT)"
        )
        conn.execute(
            "CREATE TABLE IF NOT EXISTS inventory_lines "
            "(id INTEGER PRIMARY KEY AUTOINCREMENT, inventaire_id INTEGER, "
            "product_id INTEGER, qty INTEGER)"
        )
    svc = InventoryService(dbfile)
    # load on empty inventory
    rows = svc.load_inventory_lines(1)
    assert rows == []
    # create inventory
    new_id = svc.create_inventory({"name": "test"})
    assert isinstance(new_id, int)
    # insert a line and reload
    conn = connect(dbfile)
    with conn:
        conn.execute(
            "INSERT INTO inventory_lines "
            "(inventaire_id, product_id, qty) VALUES (?, ?, ?)",
            (new_id, 42, 10)
        )
    rows2 = svc.load_inventory_lines(new_id)
    assert len(rows2) == 1
    assert rows2[0]["product_id"] == 42
