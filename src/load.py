import sqlite3

import pandas as pd

def load_hiv_data(df,conn,table_name):
    
    # take the whole dataframe and turn it into a table
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    print(f"Data loaded into table {table_name}")

    # check if rows(database) = rows(dataframe)
    row_count = pd.read_sql(f"SELECT COUNT(*) AS count FROM {table_name}", conn).iloc[0]["count"]
    assert row_count == len(df), f"ROW count mismatch: expected {len(df)}, got {row_count}"

    return row_count

df = pd.read_csv("data/processed/hiv_prevalence_clean.csv")
conn = sqlite3.connect("db/who_health.db")
table_name = "hiv_prevalence"

row_count = load_hiv_data(df,conn,table_name)

print(f"{table_name} has {row_count} rows")

# closes the connection
conn.close()