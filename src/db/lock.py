from contextlib import contextmanager
from pathlib import Path
import portalocker


# Use a lock file next to the DB file (DB path + .lock)
@contextmanager
def db_file_lock(db_path: Path | str, *, timeout: float = None):
    """Acquire a cross-process exclusive lock for operations that must
    not run concurrently.

    Usage:
        with db_file_lock(db_path):
            # do schema changes or long running exclusive ops
    """
    dbp = Path(db_path)
    lock_path = (
        dbp.with_suffix(dbp.suffix + ".lock")
        if dbp.suffix
        else Path(str(dbp) + ".lock")
    )
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    # open (create) the lock file and take an exclusive lock
    with open(lock_path, "a+") as fh:
        try:
            if timeout is None:
                portalocker.lock(fh, portalocker.LOCK_EX)
            else:
                portalocker.lock(fh, portalocker.LOCK_EX, timeout=timeout)
            yield
        finally:
            try:
                portalocker.unlock(fh)
            except Exception:
                pass
