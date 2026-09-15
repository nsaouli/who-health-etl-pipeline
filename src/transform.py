import json
import os

import pandas as pd


def clean_hiv_data(raw_data):
    df = pd.DataFrame(raw_data)
    # Drop the fully null columns
    df = df.dropna(axis=1, how="all")

    # drop the duplicate/constants columns
    df = df.drop(columns=["ParentLocationCode", "Value", "IndicatorCode"])

    # filter down to country-level rows only
    df = df[df["SpatialDimType"] == "COUNTRY"] # True or False for each row

    # drop unnecessary columns
    df = df.drop(columns=["TimeDimensionValue", "TimeDimensionBegin", "TimeDimensionEnd"])

    # they both have 1 value each so we can drop them
    df = df.drop(columns=["Date", "TimeDimType"])

    # after cleaning, I only have 1 spatial dim type which is country so i can drop it
    df = df.drop(columns=["SpatialDimType"])

    # rename columns to make data analysis easier
    df = df.rename(columns={
        "SpatialDim": "country_code",
        "ParentLocation": "region",
        "TimeDim": "year",
        "NumericValue": "hiv_prevalence_pct",
        "Low": "ci_low",
        "High": "ci_high",
    })

    # a duplicate check
    assert df.duplicated(subset=["country_code", "year"]).sum() == 0, "Duplicate country-year rows found!"
    return df
    
# opening the json file and read it as python with load
with open("data/raw/hiv_prevalence_raw.json", "r") as f:
    raw_data = json.load(f)

df = clean_hiv_data(raw_data)

# save data in a csv file
# index=False, to avoid a column of internal row position number from pandas
os.makedirs("data/processed", exist_ok=True)
df.to_csv("data/processed/hiv_prevalence_clean.csv", index=False)
print("Saved to data/processed/hiv_prevalence_clean.csv")