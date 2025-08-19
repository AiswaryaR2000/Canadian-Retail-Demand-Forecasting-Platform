from pymongo import MongoClient
import pandas as pd

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["climateData"]
collection = db["climateRawData"]

pipeline = [
    # Cast Tm to double (number) for aggregation
    {
        "$addFields": {
            "Tm_num": {
                "$convert": {
                    "input": "$Tm",
                    "to": "double",
                    "onError": None,
                    "onNull": None,
                }
            }
        }
    },
    {
        "$group": {
            "_id": {"Province": "$Province", "Year": "$Year", "Month": "$Month"},
            "avg_Tm": {"$avg": "$Tm_num"},
            "min_Tm": {"$min": "$Tm_num"},
            "max_Tm": {"$max": "$Tm_num"},
            "count": {"$sum": 1},
        }
    },
    {"$sort": {"_id.Province": 1, "_id.Year": 1, "_id.Month": 1}},
]

results = list(collection.aggregate(pipeline))

# Convert aggregation results into list of dicts for DataFrame
records = [
    {
        "Province": r["_id"]["Province"],
        "Year": r["_id"]["Year"],
        "Month": r["_id"]["Month"],
        "Avg_Temperature": r["avg_Tm"],
        "Min_Temperature": r["min_Tm"],
        "Max_Temperature": r["max_Tm"],
        "Measurement_Count": r["count"], # its the number of times they measured in a month 
    }
    for r in results
]

df = pd.DataFrame(records)

# Save to CSV
output_csv = "climate_province_monthly_summary.csv"
df.to_csv(output_csv, index=False)
print(f"Aggregated monthly data exported to {output_csv}")
