import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import zipfile
import glob

df = pd.read_csv("energy_synth.csv.zip")
df["date_time"] = pd.to_datetime(df["date_time"])

target_col = "kWhr"

RATE_CHANGE_DATE = "2025-04-15"
rate_date = pd.to_datetime(RATE_CHANGE_DATE)
df["hour"] = df["date_time"].dt.hour
df["date"] = df["date_time"].dt.date

sample = df["customer_id"].unique()

for cust in sample:
    customer_df = df[(df["customer_id"] == cust) &
                     (df["date_time"] < rate_date)]
    dates = customer_df["date"].unique()
    for date in dates:
        day_data = customer_df[customer_df["date"] == date]
        hourly = day_data.groupby("hour")[target_col].mean()
        plt.plot(hourly.index, hourly.values, color='blue', alpha=0.2)

    plt.plot([], [], color='blue', label='Days')
    plt.title(f"Hourly Energy Usage by each Customer Daily\n {cust}")
    plt.xlabel("Hour of Day")
    plt.ylabel(target_col)
    plt.xticks(range(0, 24))
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{cust}_before.png")
    plt.clf()

for cust in sample:
    customer_df = df[(df["customer_id"] == cust) &
                     (df["date_time"] >= rate_date)]
    dates = customer_df["date"].unique()
    for date in dates:
        day_data = customer_df[customer_df["date"] == date]
        hourly = day_data.groupby("hour")[target_col].mean()
        plt.plot(hourly.index, hourly.values, color='red', alpha=0.2)

    plt.plot([], [], color='red', label='Days')
    plt.title(f"Hourly Energy Usage by each Customer Daily\n {cust}")
    plt.xlabel("Hour of Day")
    plt.ylabel(target_col)
    plt.xticks(range(0, 24))
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{cust}_after.png")
    plt.clf()

# Zip all figures
with zipfile.ZipFile('figures.zip', 'w') as zf:
    for file in glob.glob('*.png'):
        zf.write(file)

print("Saved to figures.zip")