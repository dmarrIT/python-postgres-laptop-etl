from pathlib import Path
import pandas as pd

def read_raw(path: str, encoding: str = "latin1") -> pd.DataFrame:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Raw file not found: {p.resolve()}")
    return pd.read_csv(p, encoding=encoding)