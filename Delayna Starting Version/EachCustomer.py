import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# 1. Load Data
# -----------------------------
df = pd.read_csv("../.venv/energy_synth.csv")
df["date_time"] = pd.to_datetime(df["date_time"])

target_col = "kWhr"

# -----------------------------
# 2. Define Rate Change
# -----------------------------
RATE_CHANGE_DATE = "2025-04-15"
rate_date = pd.to_datetime(RATE_CHANGE_DATE)
df["hour"]  = df["date_time"].dt.hour

# -----------------------------
# 4. Plot Hourly Usage by Customer
# -----------------------------
customer_df = df[df["customer_id"] == "C0000"]
dates = customer_df["date_time"].unique()
for date in dates:
    cust = customer_df[customer_df["date_time"] == date]
    hourly= cust.groupby("hour")[target_col].mean()
    plt.plot(hourly.index,hourly.values,color='blue', alpha=0.2)

# Legend (clean version)
plt.plot([], [], color='blue', label='Days')


plt.title("Hourly Energy Usage by Customer C0000 Daily\n")
plt.xlabel("Hour of Day")
plt.ylabel(target_col)
plt.xticks(range(0, 24))
plt.grid(True, alpha=0.3)
plt.legend()

plt.tight_layout()
plt.show()

