import os
import re
import requests

# Constants
BASE_URL = "https://dd.weather.gc.ca/climate/observations/monthly/csv/"
PROVINCES = [
    "AB",
    "BC",
    "MB",
    "NB",
    "NL",
    "NS",
    "NT",
    "NU",
    "ON",
    "PE",
    "QC",
    "SK",
    "YT",
]
START_YEAR = 2017
END_YEAR = 2025
SAVE_DIR = "canada_monthly_weather"

# Create base directory
os.makedirs(SAVE_DIR, exist_ok=True)

for province in PROVINCES:
    url = f"{BASE_URL}{province}/"
    print(f"🔍 Checking {url}...")

    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"  ⚠️  Couldn't access province folder: {province}")
            continue

        # List all .csv files (exclude .csv.gz)
        files = re.findall(r'href="(climate_monthly_.*?\.csv)"', response.text)

        for original_file in files:
            print(f"Found file: {original_file}")
            match = re.search(r"_(\d{4})_", original_file)
            if not match:
                print("  ⏩ Skipping file with no valid year in name.")
                continue

            file_year = int(match.group(1))

            if START_YEAR <= file_year <= END_YEAR:
                file_url = url + original_file
                province_path = os.path.join(SAVE_DIR, province, str(file_year))
                os.makedirs(province_path, exist_ok=True)
                save_path = os.path.join(province_path, original_file)

                if os.path.exists(save_path):
                    print(f"  ✅ Already downloaded: {original_file}")
                    continue

                print(f"  ⬇️  Downloading: {original_file}")
                file_data = requests.get(file_url)
                if file_data.status_code == 200:
                    with open(save_path, "wb") as f:
                        f.write(file_data.content)
                else:
                    print(f"    ❌ Not found: {file_url}")

            else:
                print(f"  ⏩ Skipping file outside target years: {original_file}")

    except Exception as e:
        print(f"    ❌ Error accessing {url}: {e}")
