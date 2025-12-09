import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option('display.max_columns', None)

# Load datasets
accidents = pd.read_csv("data/accidents.csv")
vehicles = pd.read_csv("data/vehicles.csv")

# Standardize column names
accidents.columns = accidents.columns.str.lower().str.replace(" ", "_")
vehicles.columns = vehicles.columns.str.lower().str.replace(" ", "_")

# Parse dates
accidents["accident_date"] = pd.to_datetime(accidents["accident_date"], errors="coerce")
accidents["accident_time"] = pd.to_datetime(accidents["accident_time"], format="%H:%M", errors="coerce").dt.time

# Drop rows missing key fields
accidents = accidents.dropna(subset=["accident_id", "latitude", "longitude", "severity"])

# Ensure severity is int
accidents["severity"] = accidents["severity"].astype(int)

# Feature engineering
accidents["day_of_week"] = accidents["accident_date"].dt.day_name()
accidents["hour_of_day"] = pd.to_datetime(accidents["accident_time"], errors="coerce").dt.hour

def time_bucket(h):
    if pd.isna(h):
        return "Unknown"
    elif 5 <= h < 12:
        return "Morning"
    elif 12 <= h < 17:
        return "Afternoon"
    elif 17 <= h < 21:
        return "Evening"
    else:
        return "Night"

accidents["time_bucket"] = accidents["hour_of_day"].apply(time_bucket)

severity_map = {1: "Fatal", 2: "Serious", 3: "Slight"}
accidents["severity_label"] = accidents["severity"].map(severity_map)

# Vehicles aggregation
veh_count = vehicles.groupby("accident_id")["vehicle_id"].count().reset_index(name="vehicle_count")
veh_type_mode = vehicles.groupby("accident_id")["vehicle_type"].agg(lambda x: x.value_counts().idxmax()).reset_index(name="dominant_vehicle_type")

accidents = accidents.merge(veh_count, on="accident_id", how="left")
accidents = accidents.merge(veh_type_mode, on="accident_id", how="left")

accidents["vehicle_count"] = accidents["vehicle_count"].fillna(0)
accidents["dominant_vehicle_type"] = accidents["dominant_vehicle_type"].fillna("Unknown")

# Exploratory plots
plt.figure(figsize=(6, 4))
sns.countplot(x="severity_label", data=accidents, order=["Fatal", "Serious", "Slight"])
plt.title("Accidents by Severity")
plt.xlabel("Severity")
plt.ylabel("Count")
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 5))
sns.countplot(x="time_bucket", hue="severity_label", data=accidents,
              order=["Morning", "Afternoon", "Evening", "Night", "Unknown"])
plt.title("Accidents by Time Bucket & Severity")
plt.xlabel("Time Bucket")
plt.ylabel("Number of Accidents")
plt.tight_layout()
plt.show()

# Aggregations for BI
loc_agg = accidents.groupby(["latitude", "longitude"]).agg(
    total_accidents=("accident_id", "count"),
    fatal=("severity", lambda x: (x == 1).sum()),
    serious=("severity", lambda x: (x == 2).sum()),
    slight=("severity", lambda x: (x == 3).sum())
).reset_index()

loc_agg["severity_score"] = 3 * loc_agg["fatal"] + 2 * loc_agg["serious"] + loc_agg["slight"]

time_agg = accidents.groupby(["time_bucket", "severity_label"]).size().reset_index(name="total_accidents")
veh_agg = accidents.groupby(["dominant_vehicle_type", "severity_label"]).size().reset_index(name="total_accidents")

loc_agg.to_csv("bi_location_agg.csv", index=False)
time_agg.to_csv("bi_time_agg.csv", index=False)
veh_agg.to_csv("bi_vehicle_agg.csv", index=False)

print("Export complete: bi_location_agg.csv, bi_time_agg.csv, bi_vehicle_agg.csv")
