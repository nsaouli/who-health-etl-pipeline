# WHO Health ETL Pipeline

A Python ETL pipeline that pulls infectious disease data from the WHO Global Health Observatory (GHO) API, cleans it, and loads it into a local SQLite database.

Built as a portfolio project for a data engineering alternance application. The goal is to show a complete, well-reasoned pipeline built with real production habits, such as version control discipline, separating raw and processed data, and failing loudly on errors, rather than a single throwaway script.

## Project status

This project is in progress. Environment and Git setup, the extract step, and the transform step are complete and working. The load step (writing to SQLite), pipeline orchestration, and automated tests are still to come. This README will be expanded with full setup instructions and a data dictionary once the pipeline is complete end to end.

## What it does so far

`src/extract.py` calls the WHO GHO OData API for a chosen indicator and saves the raw JSON response, untouched, to `data/raw/`. Keeping the raw response as-is means the pipeline never needs to hit the live API again just to fix a bug further downstream.

`src/transform.py` loads that raw JSON, drops redundant or empty fields, filters the data down to country-level records, renames columns to clear names, checks that there are no duplicate country/year rows, and saves a clean table to `data/processed/` as a CSV file.

The current indicator is HIV prevalence among adults aged 15 to 49 percent, WHO indicator code MDG_0000000029, covering all countries from 2000 to the present. The values are modeled estimates from UNAIDS/WHO rather than raw case counts, and come with an associated uncertainty range. The cleaned dataset keeps the estimate along with its low and high bounds.

## Tech stack

Python 3, requests for API calls, pandas for data cleaning, SQLite for storage (coming next), and Git/GitHub for version control.

## Running what exists so far

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python src/extract.py
python src/transform.py
```

## Data source

WHO Global Health Observatory OData API: https://www.who.int/data/gho/info/gho-odata-api. Public, no authentication required.
