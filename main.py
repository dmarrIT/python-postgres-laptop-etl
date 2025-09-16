import pandas as pd

data = pd.read_csv("./data/laptop_price_raw.csv",index_col="laptop_ID",encoding="latin1")

print(data.head())
print(data.info())