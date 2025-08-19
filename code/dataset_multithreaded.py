import os
import re
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

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
MAX_WORKERS = 10  # Number of concurrent threads

# Create base directory
os.makedirs(SAVE_DIR, exist_ok=True)


def download_file(province, year, filename, base_url):
    url = f"{base_url}{province}/" + filename
    province_path = os.path.join(SAVE_DIR, province, str(year))
    os.makedirs(province_path, exist_ok=True)
    save_path = os.path.join(province_path, filename)

    if os.path.exists(save_path):
        print(f"  ✅ Already downloaded: {filename}")
        return

    print(f"  ⬇️  Downloading: {filename}")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(save_path, "wb") as f:
                f.write(response.content)
        else:
            print(f"    ❌ Not found: {url}")
    except Exception as e:
        print(f"    ❌ Error downloading {url}: {e}")


def main():
    for province in PROVINCES:
        url = f"{BASE_URL}{province}/"
        print(f"🔍 Checking {url}...")

        try:
            response = requests.get(url)
            if response.status_code != 200:
                print(f"  ⚠️  Couldn't access province folder: {province}")
                continue

            files = re.findall(r'href="(climate_monthly_.*?\.csv)"', response.text)
            tasks = []

            with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                for original_file in files:
                    match = re.search(r"_(\d{4})_", original_file)
                    if not match:
                        print(f"  ⏩ Skipping file with no valid year: {original_file}")
                        continue

                    file_year = int(match.group(1))
                    if START_YEAR <= file_year <= END_YEAR:
                        # Schedule download
                        tasks.append(
                            executor.submit(
                                download_file,
                                province,
                                file_year,
                                original_file,
                                BASE_URL,
                            )
                        )
                    else:
                        print(
                            f"  ⏩ Skipping file outside target years: {original_file}"
                        )

                # Optionally wait for all to finish (to catch exceptions)
                for future in as_completed(tasks):
                    future.result()

        except Exception as e:
            print(f"    ❌ Error accessing {url}: {e}")


if __name__ == "__main__":
    main()
