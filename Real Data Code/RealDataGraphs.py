import os
import pandas as pd
import matplotlib.pyplot as plt
import delta_sharing

# -----------------------------
# 1. Load Data via Delta Sharing
# -----------------------------
profile_file = "../.venv/config.share"
table_url = "config.share#ccu-delta-share.account_metering.intervals_redacted"

df = delta_sharing.load_as_pandas(
    table_url,
    # some versions support limit:
)
df = df.sort_values("start_datetime")
# -----------------------------
# 2. Prep for Graphing
# -----------------------------
df = df.rename(columns={
    "kwh": "kWhr",
    "meter_number": "customer_id",
    "start_datetime": "date_time",
})

df["date_time"] = pd.to_datetime(df["date_time"])
df["kWhr"] = pd.to_numeric(df["kWhr"], errors="coerce")
df["hour"] = df["date_time"].dt.hour
df["date"] = df["date_time"].dt.date

target_col = "kWhr"

# First 10 customers
sample = df["customer_id"].unique()[:1]
'''
# -----------------------------
# 3. Rate Change Date - THE DAY THE PEAK CHANGES
# -----------------------------
RATE_CHANGE_DATE = "2025-04-15"
rate_date = pd.to_datetime(RATE_CHANGE_DATE)

# -----------------------------
# 4. Pre Rate Change Plots (Blue)
# -----------------------------
for cust in sample:
    customer_df = df[(df["customer_id"] == cust) &
                     (df["date_time"] < rate_date)]
    dates = customer_df["date"].unique()
    for date in dates:
        day_data = customer_df[customer_df["date"] == date]
        hourly = day_data.groupby("hour")[target_col].mean()
        plt.plot(hourly.index, hourly.values, color='blue', alpha=0.2)

    plt.plot([], [], color='blue', label='Days')
    plt.title(f"Hourly Energy Usage — Pre Rate Change\n{cust}")
    plt.xlabel("Hour of Day")
    plt.ylabel(target_col)
    plt.xticks(range(0, 24))
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()

# -----------------------------
# 5. Post Rate Change Plots (Red)
# -----------------------------
for cust in sample:
    customer_df = df[(df["customer_id"] == cust) &
                     (df["date_time"] >= rate_date)]
    dates = customer_df["date"].unique()
    for date in dates:
        day_data = customer_df[customer_df["date"] == date]
        hourly = day_data.groupby("hour")[target_col].mean()
        plt.plot(hourly.index, hourly.values, color='red', alpha=0.2)

    plt.plot([], [], color='red', label='Days')
    plt.title(f"Hourly Energy Usage — Post Rate Change\n{cust}")
    plt.xlabel("Hour of Day")
    plt.ylabel(target_col)
    plt.xticks(range(0, 24))
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()
'''
for cust in sample:
    customer_df = df[df["customer_id"] == cust]
    dates = customer_df["date"].unique()

    for date in dates:
        day_data = customer_df[customer_df["date"] == date]
        hourly = day_data.groupby("hour")[target_col].mean()
        plt.plot(hourly.index, hourly.values, color='red', alpha=0.2)

    plt.plot([], [], color='red', label='Days')
    plt.title(f"Hourly Energy Usage — Post Rate Change\n{cust}\n{dates.min()} to {dates.max()}")
    plt.xlabel("Hour of Day")
    plt.ylabel(target_col)
    plt.xticks(range(0, 24))
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()