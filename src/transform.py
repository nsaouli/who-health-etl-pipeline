import json
import os

import pandas as pd


def clean_hiv_data(raw_data):

    df = pd.DataFrame(raw_data)

    df = df.dropna(axis=1, how="all")
    # duplicate/constant columns
    df = df.drop(columns=["ParentLocationCode", "Value", "IndicatorCode"])
    # dropping GLOBAL/REGION rows so every row is a comparable single country
    df = df[df["SpatialDimType"] == "COUNTRY"]
    # Time begins 01/01 and ends 31/12 accross all countries, only the year changes
    # TimeDimensionValue is the year, we drop it because year is already a column 
    df = df.drop(columns=["TimeDimensionValue", "TimeDimensionBegin", "TimeDimensionEnd"])
    # 'Date' and 'TimeDimType' are constant accross all rows
    df = df.drop(columns=["Date", "TimeDimType"])
    # After filtering to country, SpatialDimType is a constant: 'Country'
    df = df.drop(columns=["SpatialDimType"])

    # renamed for clarity, since these become the real SQLite column names later
    df = df.rename(columns={
        "SpatialDim": "country_code",
        "ParentLocation": "region",
        "TimeDim": "year",
        "NumericValue": "hiv_prevalence_pct",
        "Low": "ci_low",
        "High": "ci_high",
    })

    assert df.duplicated(subset=["country_code", "year"]).sum() == 0, "Duplicate country-year rows found!"

    return df

with open("data/raw/hiv_prevalence_raw.json", "r") as f:
    raw_data = json.load(f)

df = clean_hiv_data(raw_data)
os.makedirs("data/processed", exist_ok=True)
df.to_csv("data/processed/hiv_prevalence_clean.csv", index=False)
print("Saved to data/processed/hiv_prevalence_clean.csv")