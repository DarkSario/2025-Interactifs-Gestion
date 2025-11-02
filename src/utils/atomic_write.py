from pathlib import Path
import tempfile
import os


def atomic_write(path: Path | str, data: bytes | str, mode: str = "wb", encoding: str = "utf-8"):
    """
    Écrit atomiquement `data` dans `path`:
    - écrit dans un fichier temporaire dans le même dossier
    - fsync pour s'assurer de la persistance
    - rename/replace atomique
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    dirpath = str(path.parent)
    fd, tmp_path = tempfile.mkstemp(dir=dirpath)
    try:
        # open file descriptor with desired mode
        with os.fdopen(fd, mode) as f:
            if isinstance(data, str):
                f.write(data.encode(encoding) if "b" in mode else data)
            else:
                f.write(data)
            f.flush()
            os.fsync(f.fileno())
        # replace atomiquement
        os.replace(tmp_path, str(path))
    except Exception:
        # cleanup on error
        try:
            os.remove(tmp_path)
        except Exception:
            pass
        raise
