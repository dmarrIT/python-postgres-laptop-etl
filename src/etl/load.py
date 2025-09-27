from pathlib import Path
import pandas as pd
import sqlite3

def to_csv(df: pd.DataFrame, out_dir: str, filename: str) -> str:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    path = out / filename
    df.to_csv(path, index=False)
    return str(path)

def to_sqlite(df: pd.DataFrame, sqlite_path: str, table_name: str, if_exists: str = "replace") -> None:
    spath = Path(sqlite_path)
    spath.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(spath)
    try:
        df.to_sql(table_name, con, if_exists=if_exists, index=False)
    finally:
        con.close()