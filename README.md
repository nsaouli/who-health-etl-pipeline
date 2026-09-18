# WHO Health ETL Pipeline

A Python ETL pipeline that pulls infectious disease data from the WHO Global Health Observatory (GHO) API, cleans it, and loads it into a local SQLite database.

Built as a portfolio project for a data engineering alternance application. The goal is to show a complete, well-reasoned pipeline built with real production habits, such as version control discipline, separating raw and processed data, and failing loudly on errors, rather than a single throwaway script.

## Project status

The pipeline is complete end to end.
All following steps are done: 
* Environment and Git setup
* The extract step
* The transform step
* The load step (writing to SQLite)
* The pipeline orchestration
* The automated tests (for transform & load)

## What it does

`src/extract.py` calls the WHO GHO OData API for a chosen indicator and saves the raw JSON response, untouched, to `data/raw/`. Keeping the raw response as-is means the pipeline never needs to hit the live API again just to fix a bug further downstream.

`src/transform.py` loads that raw JSON, drops redundant or empty fields, filters the data down to country-level records, renames columns to clear names, checks that there are no duplicate country/year rows, and saves a clean table to `data/processed/` as a CSV file.

`src/load.py` creates a table of the dataframe, named `hiv_prevalence`, in the SQLite database in `db/`, checks if the number of rows adds up within the table and the dataframe, then closes the connection with sqlite.

`src/main.py` runs the whole pipeline in order (extract, transform, load) using `check=True` so the pipeline stops immediately if any script fails, rather than continuing on broken data.

`tests/test_transform.py` and `tests/test_load.py` use small, hand-written fake datasets to verify that `src/transform.py` and `src/load.py` behave correctly, without touching the real API or database.

## Tech stack

* Python 3
* requests for API calls
* pandas for data cleaning
* Git/GitHub for version control
* sqlite3 for SQL database
* subprocess for orchestration and automation
* pytest for test files

## How to run the project

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# optional: run tests
python -m pytest

# run the pipeline
python src/main.py

```

## Project structure

```
who-health-etl/
├── data/
│   ├── raw/              ← untouched API responses (JSON)
│   └── processed/        ← cleaned data
├── src/
│   ├── __init__.py       ← marks src/ as an importable package, needed for the tests to import from it
│   ├── extract.py        ← calls the WHO API, saves raw JSON
│   ├── transform.py      ← cleans + reshapes into tidy rows
│   ├── load.py           ← writes into SQLite
│   └── main.py           ← runs the whole pipeline in order
├── db/                   ← SQLite database lives here
├── tests/ 
│   ├── test_transform.py ← tests if transform.py is working correctly
│   └── test_load.py      ← tests if load.py is working correctly
├── .gitignore
├── requirements.txt
└── README.md
```

## About the data

The current indicator is HIV prevalence among adults aged 15 to 49 percent, WHO indicator code MDG_0000000029, covering all countries from 2000 to the present. The values are modeled estimates from UNAIDS/WHO rather than raw case counts, and come with an associated uncertainty range. The cleaned dataset keeps the estimate along with its low and high bounds.

### Data source

WHO Global Health Observatory OData API: https://www.who.int/data/gho/info/gho-odata-api. Public, no authentication required.

### Data dictionary

|Column            |Meaning                                     |Notes                                                  |
|---|---|---|
|Id                |WHO's internal database row number           |It spans every indicator they track                    |
|country_code      |ISO 3-letter country code                   |e.g. FRA, AGO                                          |
|region            |WHO region grouping                         |e.g. Europe, Africa                                    |
|year              |Year of the estimate                        |e.g. 2000 - present                                    |
|hiv_prevalence_pct|Estimated % of adults 15-49 living with HIV |Modeled estimate, not a raw count                      |
|ci_low/ci_high    |Lower/upper bounds of the uncertainty range |Reflects data quality/surveillance strength per country|