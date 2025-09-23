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
data.rename(columns={'laptop_ID': 'laptop_id'}, inplace=True)

data.rename(columns={'Company': 'company'}, inplace=True)
data['company'] = (
    data['company']
        .str.strip()
        .str.replace(r'\s+', ' ', regex=True)
)

data.rename(columns={'Product': 'product'}, inplace=True)
data['product'] = (
    data['product']
        .str.strip()
        .str.replace(r'\s+', ' ', regex=True)
)

data.rename(columns={'TypeName': 'device_type'}, inplace=True)
data['device_type'] = (
    data['device_type']
        .str.strip()
        .str.replace(r'\s+', ' ', regex=True)
)

data.rename(columns={'Inches': 'screen_size_in'}, inplace=True)

data.rename(columns={'ScreenResolution': 'screen_resolution'}, inplace=True)
data['screen_resolution'] = (
    data['screen_resolution']
        .str.strip()
        .str.replace(r'\s+', ' ', regex=True)
)

data.rename(columns={'Weight':'weight_kg'}, inplace=True)
data['weight_kg'] = (
    data['weight_kg']
        .str.lower()
        .str.replace('kg', '', regex=False)
        .str.strip()
        .astype(float)
)

#TODO standardize everything after screen_resolution and before weight_kg

# Add parsed numeric columns for screen_width and screen_height from screen_resolution
data[['screen_width','screen_height']] = (
    data['screen_resolution']
      .str.extract(r'(\d+)x(\d+)')
      .astype('Int64')
)



# Check data after changes
print(data.head())


# ========== Load ==========