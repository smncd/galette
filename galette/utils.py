from pathlib import Path

def set_path(path: Path|str, fallback: Path|str|None = None, create_fallback: bool = False) -> Path:
    path = Path(path)

    if fallback:
        fallback = Path(fallback)

    if path.exists() and path.is_dir():
        return path
    elif fallback and fallback.exists() and fallback.is_dir():
        return fallback
    elif create_fallback:
        fallback.mkdir()
        return fallback
    else:
        raise ValueError(f"{fallback if fallback else path} is not a folder, exiting...")