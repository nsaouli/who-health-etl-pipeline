import sqlite3

import pandas as pd

df = pd.read_csv("data/processed/hiv_prevalence_clean.csv")

conn = sqlite3.connect("db/who_health.db")

# take the whole dataframe and turn it into a table
df.to_sql("hiv_prevalence", conn, if_exists="replace", index=False)
print("Data loaded into table 'hiv_prevalence'")

# check if rows(database) = rows(dataframe)
row_count = pd.read_sql("SELECT COUNT(*) AS count FROM hiv_prevalence", conn).iloc[0]["count"]
assert row_count == len(df), f"ROW count mismatch: expected {len(df)}, got {row_count}"

# closes the connection
conn.close()