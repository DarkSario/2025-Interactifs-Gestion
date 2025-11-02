from pathlib import Path
import portalocker

def write_with_lock(path: Path | str, data: bytes):
    """
    Écriture protégée par verrouillage (utile si plusieurs processus peuvent écrire).
    Requires portalocker.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as f:
        portalocker.lock(f, portalocker.LOCK_EX)
        try:
            f.write(data)
            f.flush()
            f.fsync()
        finally:
            portalocker.unlock(f)