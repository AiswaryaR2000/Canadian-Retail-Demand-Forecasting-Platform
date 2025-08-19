import os
import re
import pandas as pd
from pymongo import MongoClient
from concurrent.futures import ThreadPoolExecutor, as_completed

SAVE_DIR = "canada_monthly_weather"
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
FILENAME_RE = re.compile(r"climate_monthly_([A-Z]{2})_([0-9A-Z]+)_([0-9]{4})_P1M\.csv")

# Thread-safe MongoClient (each thread uses its own DB/Collection handle)
client = MongoClient("mongodb://localhost:27017/")
db = client["climateData"]
collection = db["climateRawData"]


def clean_dataframe(df):
    return df.replace({"NA": None, "": None})


def process_csv(file_info):
    province, year, file_path, filename = file_info

    match = FILENAME_RE.match(filename)
    if not match:
        return f"SKIPPED (no match): {filename}"

    prov_code, station_id, file_year = match.groups()

    try:
        df = pd.read_csv(file_path)
        df = clean_dataframe(df)
        df["_source_file"] = filename
        df["_province_folder"] = province
        df["_station_id"] = station_id
        df["_year_from_folder"] = year
        df["_year_from_filename"] = int(file_year)

        records = df.to_dict(orient="records")
        if records:
            # Each thread uses its own collection instance
            collection.insert_many(records)
            return f"[{province}/{year}] Inserted {len(records)} from {filename}"
        else:
            return f"[{province}/{year}] EMPTY: {filename}"
    except Exception as e:
        return f"[{province}/{year}] ERROR in {filename}: {e}"


# Gather all file paths
file_list = []
for province in PROVINCES:
    for year in range(2017, 2026):
        year_dir = os.path.join(SAVE_DIR, province, str(year))
        if not os.path.isdir(year_dir):
            continue
        for filename in os.listdir(year_dir):
            if filename.endswith(".csv"):
                file_path = os.path.join(year_dir, filename)
                file_list.append((province, year, file_path, filename))

# Process with threads
with ThreadPoolExecutor(max_workers=8) as executor:  # Adjust thread count as needed
    futures = [executor.submit(process_csv, info) for info in file_list]
    for future in as_completed(futures):
        print(future.result())
