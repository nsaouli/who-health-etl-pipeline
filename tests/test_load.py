# tests/test_load.py
import pandas as pd

import sqlite3

from src.load import load_hiv_data


def test_load_hiv_data_returns_correct_row_count():

    df= pd.DataFrame ([
            {      
                "SpatialDim": "FRA",
                "ParentLocation": "Europe",
                "TimeDim": 2020,
                "NumericValue": 0.3,
                "Low": 0.3,
                "High": 0.3,
            },

            {      
                "SpatialDim": "US",
                "ParentLocation": "America",
                "TimeDim": 2024,
                "NumericValue": 0.65,
                "Low": 0.6,
                "High": 0.7,
            },

            {      
                "SpatialDim": "ESP",
                "ParentLocation": "Europe",
                "TimeDim": 2025,
                "NumericValue": 0.4,
                "Low": 0.4,
                "High": 0.4,
            }
         ])

    conn = sqlite3.connect(":memory:")            # creates a database that only exists in memory
    table_name = "testing_table"

    row_count = load_hiv_data(df,conn,table_name)

    assert row_count == 3

    conn.close()