import json
import os

import requests

# Indicator Name: Prevalence of HIV among adults aged 15 to 49 (%).
INDICATOR_CODE = "MDG_0000000029"
url = f"https://ghoapi.azureedge.net/api/{INDICATOR_CODE}"

response = requests.get(url)
response.raise_for_status()
data = response.json()

os.makedirs("data/raw", exist_ok=True)

# the actual data exists within the second key, named 'value'.
# we drop the first key, which contains the metadata '@odata.context'.
with open("data/raw/hiv_prevalence_raw.json","w") as f:
    json.dump(data["value"], f, indent=2)  

print("Saved to data/raw/hiv_prevalence_raw.json")

