# Laptop Price ETL Pipeline

A simple Extract-Transform-Load (ETL) pipeline that ingests a raw laptop-price dataset, cleans and standardizes the fields, and produces a fully transformed CSV and SQL db file ready for analysis or downstream data-engineering tasks.

This project demonstrates a production-style ETL workflow for data-engineering practice and portfolio use.

Raw dataset used is availble at: https://www.kaggle.com/datasets/muhammetvarl/laptop-price

## How It Works

### 1. Extract

- Reads the raw laptop_price_raw.csv (Latin-1 encoded) into a Pandas DataFrame.

### 2. Transform
- Drops duplicates and trims whitespace.
- Standardizes column names and text fields.
- Parses numeric columns (RAM, weight, screen dimensions, price).
- Splits composite fields (e.g., screen resolution → width/height).
- Derives new fields such as price in USD.

### 3. Load

- Writes the clean dataset to data/processed/laptop_price_clean.csv, ready for analytics, dashboards, or database ingestion.

## Setup and Run

1. **Clone the repo**
```bash
git clone https://github.com/dmarrIT/python-postgres-laptop-etl.git
cd python-postgres-laptop-etl
```

2. **Create and activate virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. **Run the pipeline**
```bash
python -m src.pipeline
```