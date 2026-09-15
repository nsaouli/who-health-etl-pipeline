# tests/test_transform.py

from src.transform import clean_hiv_data

def test_clean_hiv_data_filters_to_countries():
    raw_data = [
        {
            "IndicatorCode": "MDG_0000000029",
            "SpatialDimType": "GLOBAL",
            "SpatialDim": "GLOBAL",                 
            "ParentLocationCode":None,
            "TimeDimType":"YEAR",
            "ParentLocation": None,
            "TimeDim":2020,
            "Value":"1.3 [1 - 1.6]",
            "NumericValue":1.300000000,
            "Low":1.000000000,
            "High":1.600000000,
            "Date":"2026-01-01",
            "TimeDimensionValue":"2000",
            "TimeDimensionBegin":"2000-01-01",
            "TimeDimensionEnd":"2026-01-01",
        },
        {
            "IndicatorCode": "MDG_0000000029",
            "SpatialDimType": "COUNTRY",
            "SpatialDim": "FRA",
            "ParentLocationCode": "EUR",
            "TimeDimType": "YEAR",
            "ParentLocation": "Europe",
            "TimeDim": 2020,
            "Value": "0.3 [0.3 - 0.3]",
            "NumericValue": 0.3,
            "Low": 0.3,
            "High": 0.3,
            "Date": "2026-01-01",
            "TimeDimensionValue": "2020",
            "TimeDimensionBegin": "2020-01-01",
            "TimeDimensionEnd": "2020-12-31",
        },
    ]

    df = clean_hiv_data(raw_data)

    assert len(df) == 1
    assert df.iloc[0]["country_code"] == "FRA"