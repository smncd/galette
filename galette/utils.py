from pathlib import Path
from uuid import uuid5, NAMESPACE_URL

def uuid_for(string: str|Path) -> str: 
    return str(uuid5(namespace=NAMESPACE_URL, name=str(string)))

def set_path(path: Path|str|None, fallback: Path|str|None = None, create_fallback: bool = False) -> Path:
    if path:
        path = Path(path)

    if fallback:
        fallback = Path(fallback)

    if path and path.exists() and path.is_dir():
        return path
    elif fallback and fallback.exists() and fallback.is_dir():
        return fallback
    elif create_fallback:
        fallback.mkdir()
        return fallback
    else:
        raise ValueError(f"{path} is not directory")
    
def dir_exists(input: str) -> bool:
    path = Path(input)

    return path.exists() and path.is_dir()