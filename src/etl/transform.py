import pandas as pd

def clean(data: pd.DataFrame, eur_to_usd: float = 1.08) -> pd.DataFrame:
    df = data.copy()

    # Drop exact duplicate rows
    df.drop_duplicates(inplace=True)

    # ---------- Standardize column names ----------
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
    df.rename(columns=rename_map, inplace=True)

    # ---------- Clean text fields ----------
    def clean_text(s: pd.Series) -> pd.Series:
        return s.astype(str).str.strip().str.replace(r'\s+', ' ', regex=True)

    for col in ['company', 'product', 'device_type', 'screen_resolution', 'cpu', 'gpu', 'operating_system']:
        if col in df.columns:
            df[col] = clean_text(df[col])

    # ---------- Numeric coercions ----------
    # screen inches
    if 'screen_size_in' in df.columns:
        df['screen_size_in'] = pd.to_numeric(df['screen_size_in'], errors='coerce')

    # RAM (e.g., "8GB" -> 8)
    if 'ram_gb' in df.columns:
        df['ram_gb'] = (
            df['ram_gb'].astype(str).str.lower()
              .str.replace('gb', '', regex=False)
              .str.strip()
        )
        df['ram_gb'] = pd.to_numeric(df['ram_gb'], errors='coerce').astype('Int64')

    # Storage split 
    if 'storage' in df.columns:
        df['storage_gb'] = (
            df['storage'].astype(str).str.extract(r'(\d+)\s*GB').astype('Int64')
        )
        df['storage_type'] = (
            df['storage'].astype(str).str.replace(r'\d+\s*GB', '', regex=True).str.strip()
        )

    # Weight (e.g., "1.25kg" -> 1.25)
    if 'weight_kg' in df.columns:
        df['weight_kg'] = (
            df['weight_kg'].astype(str).str.lower()
              .str.replace('kg', '', regex=False)
              .str.strip()
        )
        df['weight_kg'] = pd.to_numeric(df['weight_kg'], errors='coerce')

    # Price (strip symbols/commas -> float)
    if 'price_euros' in df.columns:
        df['price_euros'] = (
            df['price_euros'].astype(str)
                .str.replace(r'[^\d\.\,]', '', regex=True)  # keep digits/./,
                .str.replace(',', '', regex=False)
                .str.strip()
        )
        df['price_euros'] = pd.to_numeric(df['price_euros'], errors='coerce')
        df['price_usd'] = (df['price_euros'] * eur_to_usd).round(2)

    # Screen resolution -> width/height
    if 'screen_resolution' in df.columns:
        df[['screen_width', 'screen_height']] = (
            df['screen_resolution'].astype(str)
              .str.extract(r'(\d+)\s*x\s*(\d+)')
              .astype('Int64')
        )

    # Final tidy-up
    df.reset_index(drop=True, inplace=True)

    return df