"""Week 1: extract a random sample of listing remarks to CSV."""
import warnings
from pathlib import Path

import mysql.connector
import pandas as pd

warnings.filterwarnings("ignore", message=".*pandas only supports SQLAlchemy.*")

OUT = Path("data/processed/listing_sample.csv")
OUT.parent.mkdir(parents=True, exist_ok=True)

conn = mysql.connector.connect(
    host="127.0.0.1", port=3306, user="root", password="root", database="real_estate"
)

query = """
SELECT L_ListingID, L_Address, L_City, L_Keyword2 AS beds,
       LM_Dec_3 AS baths, L_SystemPrice AS price, L_Remarks AS remarks
FROM rets_property
WHERE L_Remarks IS NOT NULL AND LENGTH(L_Remarks) > 50
ORDER BY RAND(42)
LIMIT 1000
"""

try:
    df = pd.read_sql(query, conn)
finally:
    conn.close()

df["remarks"] = (
    df["remarks"]
    .str.replace(r"(\\r|\\n|\r|\n)+", " ", regex=True)  # literal and real line breaks
    .str.replace(r"\s+", " ", regex=True)                # collapse extra spaces
    .str.strip()
)
df.to_csv(OUT, index=False)

print(f"Saved {len(df)} rows to {OUT}")
print(f"Remark length: min {df.remarks.str.len().min()}, "
      f"median {int(df.remarks.str.len().median())}, max {df.remarks.str.len().max()}")
print(df.head(3).to_string())
