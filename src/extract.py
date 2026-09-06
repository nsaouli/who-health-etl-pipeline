import json
import os

import requests

INDICATOR_CODE = "MDG_0000000029"
url = f"https://ghoapi.azureedge.net/api/{INDICATOR_CODE}"

response = requests.get(url)
response.raise_for_status()

# Transforming the data from json to python object, here a dictionary
data = response.json()

# a safety habit, the folder already exists
# but exist_ok=True means 'don't error out if it's already there'
# useful for other people and if i wanna run it on a new machine from scratch
os.makedirs("data/raw", exist_ok=True)

# json.dump taking out a python object and turning it into a json text into a file
# indent=2 makes the saved file human-readable, small kindness to future me
with open("data/raw/hiv_prevalence_raw.json","w") as f:
    json.dump(data["value"], f, indent=2)  

print("Saved to data/raw/hiv_prevalence_raw.json")

