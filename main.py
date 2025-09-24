import pandas as pd

# ========== Extract ========== 

data = pd.read_csv("./data/laptop_price_raw.csv",index_col="laptop_ID",encoding="latin1")


# ========== Transform ==========

# Inspect the schema, check for outliers, and numeric vs object columns
print(data.head())
print(data.describe())
print(data.info())

# Detect missing values
print("\nMissing values:")
print(data.isna().sum())

# Detect duplicate values
print("\nDuplicate values:")
print(data.duplicated().sum())

# View duplicate rows
print(data[data.duplicated()])

# Drop duplicate rows
data.drop_duplicates(inplace=True)

# Ensure duplicate rows dropped successfully
print("\nDuplicate values after dropping:")
print(data.duplicated().sum())

# Standardize
rename_map = {
    'laptop_ID': 'laptop_id',
    'Company': 'company',
    'Product': 'product',
    'TypeName': 'device_type',
    'Inches': 'screen_size_in',
    'ScreenResolution': 'screen_resolution',
    'Cpu': 'cpu',
    'Ram': 'ram_gb',
    'Memory': 'storage',
    'Gpu': 'gpu',
    'OpSys': 'operating_system',
    'Weight': 'weight_kg',
    'Price_euros': 'price_euros',
}
data.rename(columns=rename_map, inplace=True)

data['company'] = (
    data['company']
        .str.strip()
        .str.replace(r'\s+', ' ', regex=True)
)

data['product'] = (
    data['product']
        .str.strip()
        .str.replace(r'\s+', ' ', regex=True)
)

data['device_type'] = (
    data['device_type']
        .str.strip()
        .str.replace(r'\s+', ' ', regex=True)
)

data['screen_resolution'] = (
    data['screen_resolution']
        .str.strip()
        .str.replace(r'\s+', ' ', regex=True)
)

data['cpu'] = (
    data['cpu']
        .str.strip()
        .str.replace(r'\s+', ' ', regex=True)
)

data['ram_gb'] = (
    data['ram_gb']
        .str.lower()
        .str.replace('gb', '', regex=False)
        .str.strip()
        .astype('Int64')
)

# split storage into two new fields: storage_gb and storage_type
data['storage_gb'] = (
    data['storage']
        .str.extract(r'(\d+)\s*GB')
        .astype('Int64')
)

data['storage_type'] = (
    data['storage']
        .str.replace(r'\d+\s*GB', '', regex=True)
        .str.strip()
)

data['gpu'] = (
    data['gpu']
        .str.strip()
        .str.replace(r'\s+', ' ', regex=True)
)

data['operating_system'] = (
    data['operating_system']
        .str.strip()
        .str.replace(r'\s+', ' ', regex=True)
)

data['weight_kg'] = (
    data['weight_kg']
        .str.lower()
        .str.replace('kg', '', regex=False)
        .str.strip()
        .astype(float)
)

# Derive price in USD
eur_to_usd = 1.08
data['price_usd'] = (data['price_euros'] * eur_to_usd).round(2)

# Add parsed numeric columns for screen_width and screen_height from screen_resolution
data[['screen_width','screen_height']] = (
    data['screen_resolution']
      .str.extract(r'(\d+)x(\d+)')
      .astype('Int64')
)

# Check data after changes
print(data.head())
print(data.describe())
print(data.info())

# ========== Load ==========