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

    pre  = df[(df["customer_id"] == cust) & (df["date_time"] <  rate_date)]
    post = df[(df["customer_id"] == cust) & (df["date_time"] >= rate_date)]

    if len(pre) == 0 or len(post) == 0:
        plt.close()
        continue

    pre_mean  = pre.groupby("hour")[target_col].mean().reindex(range(24), fill_value=0)
    post_mean = post.groupby("hour")[target_col].mean().reindex(range(24), fill_value=0)

    diff = post_mean - pre_mean

    if diff.std() < 1e-6:
        plt.close()
        continue

    norm_diff = (diff - diff.mean()) / diff.std()

    ax.plot(range(24), diff.values,      color="purple", linewidth=2.5, label="Difference (Post - Pre)")
    ax.plot(range(24), norm_diff.values, color="orange", linewidth=2.0, label="Normalized Difference", linestyle="--")
    ax.axhline(0, color="black", linewidth=1, linestyle=":")

    ax.set_title(f"Hourly Usage Difference — Customer {cust}")
    ax.set_xlabel("Hour of Day")
    ax.set_ylabel(target_col)
    ax.set_xticks(range(0, 24))
    ax.grid(True, alpha=0.3)
    ax.legend()

    plt.tight_layout()
    plt.show()