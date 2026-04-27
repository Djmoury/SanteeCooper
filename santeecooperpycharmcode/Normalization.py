import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


df = pd.read_csv("energy_synth.csv.zip")
df["date_time"] = pd.to_datetime(df["date_time"])

target_col = "kWhr"


RATE_CHANGE_DATE = "2025-04-15"
rate_date = pd.to_datetime(RATE_CHANGE_DATE)
df["hour"] = df["date_time"].dt.hour
df["date"] = df["date_time"].dt.date


sample = df["customer_id"].unique()

for cust in sample:
    fig, ax = plt.subplots(figsize=(12, 5))

    for period, color, label in [
        (df["date_time"] < rate_date,  "blue", "Pre Rate Change"),
        (df["date_time"] >= rate_date, "red",  "Post Rate Change"),
    ]:
        customer_df = df[(df["customer_id"] == cust) & period]

        if len(customer_df) == 0:
            continue

        mean_hourly = customer_df.groupby("hour")[target_col].mean()

        # Mean line
        ax.plot(mean_hourly.index, mean_hourly.values,
                color=color, linewidth=2.5, label=label)



    ax.set_title(f"Avg Hourly Energy Usage — Customer {cust}")
    ax.set_xlabel("Hour of Day")
    ax.set_ylabel(target_col)
    ax.set_xticks(range(0, 24))
    ax.grid(True, alpha=0.3)
    ax.legend()

    plt.tight_layout()
    plt.show()