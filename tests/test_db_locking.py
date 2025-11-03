import threading
import time
from src.db.connection import connect


def test_busy_timeout_allows_wait(tmp_path):
    dbfile = tmp_path / "locked.db"
    # Prepare DB and a simple table
    conn_a = connect(dbfile)
    with conn_a:
        conn_a.execute("CREATE TABLE IF NOT EXISTS t (id INTEGER PRIMARY KEY, v TEXT)")
    conn_a.close()
    # ensure long-running transaction holds a lock
    exc = None

    def hold_transaction_and_commit():
        conn1 = connect(dbfile, timeout=1, check_same_thread=False)
        c = conn1.cursor()
        try:
            c.execute("BEGIN")
            c.execute("INSERT INTO t (v) VALUES (?)", ("a",))
            # sleep while other thread tries to write
            time.sleep(0.5)
            conn1.commit()
        finally:
            c.close()
            conn1.close()

    def try_writer():
        nonlocal exc
        try:
            conn2 = connect(dbfile, timeout=1, check_same_thread=False)
            c2 = conn2.cursor()
            try:
                c2.execute("BEGIN")
                c2.execute("INSERT INTO t (v) VALUES (?)", ("b",))
                conn2.commit()
            finally:
                c2.close()
                conn2.close()
        except Exception as e:
            exc = e

    t1 = threading.Thread(target=hold_transaction_and_commit)
    t2 = threading.Thread(target=try_writer)
    t1.start()
    time.sleep(0.05)
    t2.start()
    t1.join()
    t2.join()

    assert exc is None, f"writer failed with {exc}"

    # final sanity check: both rows present
    conn_check = connect(dbfile)
    try:
        cr = conn_check.cursor()
        try:
            cr.execute("SELECT COUNT(*) FROM t")
            assert cr.fetchone()[0] == 2
        finally:
            cr.close()
    finally:
        conn_check.close()
