import pandas as pd
from pathlib import Path

def extract_first_digits(data):
    if data >= 10:
       return int(str(data)[:2])

root_dir = Path(__file__).parent.parent.parent
file_name = root_dir / "data" / "dc_subset.csv"

purchases_df = pd.read_csv(file_name, usecols=["TRANSACTION_AMOUNT"])
purchases_df = purchases_df.map(extract_first_digits)
print(purchases_df)

    




# lambda x: int(str(x)[:2])