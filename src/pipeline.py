from pathlib import Path
import yaml
import logging

from src.etl.extract import read_raw
from src.etl.transform import clean
from src.etl.load import to_csv, to_sqlite

Path("logs").mkdir(exist_ok=True)
logging.basicConfig(
    filename="logs/etl.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logging.info("ETL pipeline started")

def main():
    cfg_path = Path("config/settings.yaml")
    with cfg_path.open() as f:
        cfg = yaml.safe_load(f)

    raw_path = cfg["data"]["raw_path"]
    eur_to_usd = cfg["currency"]["eur_to_usd"]

    # Extract
    df_raw = read_raw(raw_path)

    # Transform
    df_clean = clean(df_raw, eur_to_usd=eur_to_usd)

    # Load (CSV)
    out_dir = cfg["data"]["processed_dir"]
    out_name = cfg["data"]["processed_filename"]
    out_csv = to_csv(df_clean, out_dir, out_name)

    # Load (SQLite)
    if cfg.get("db", {}).get("use_sqlite", False):
        to_sqlite(
            df_clean,
            sqlite_path=cfg["db"]["sqlite_path"],
            table_name=cfg["db"]["table_name"],
        )

    print(f"✓ Wrote cleaned data to {out_csv}")

if __name__ == "__main__":
    main()