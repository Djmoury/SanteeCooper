import pandas as pd
import matplotlib.pyplot as plt

# 1. Load and Setup
df = pd.read_csv("../.venv/energy_synth.csv")
df["date_time"] = pd.to_datetime(df["date_time"])

target_col = "kWhr" # Using your updated column name
RATE_CHANGE_DATE = "2025-04-15"
rate_date = pd.to_datetime(RATE_CHANGE_DATE)

# 2. Split Data
df_before = df[df["date_time"] < rate_date]
df_after  = df[df["date_time"] >= rate_date]

# 3. Resample to Daily Averages
daily_before = df_before.resample('D', on='date_time')[target_col].mean().reset_index()
daily_after  = df_after.resample('D', on='date_time')[target_col].mean().reset_index()

# 4. Create Relative Day Count
daily_before['day_num'] = (daily_before['date_time'] - daily_before['date_time'].min()).dt.days
daily_after['day_num']  = (daily_after['date_time'] - daily_after['date_time'].min()).dt.days

# --- NEW SECTION: CALCULATE DIFFERENCE ---

# Merge the two periods on the Day Number to compare them directly
diff_df = pd.merge(
    daily_before[['day_num', target_col]],
    daily_after[['day_num', target_col]],
    on='day_num',
    suffixes=('_before', '_after')
)

# Calculate the actual difference (Delta)
diff_df['delta'] = diff_df[f'{target_col}_after'] - diff_df[f'{target_col}_before']
diff_df['delta_smooth'] = diff_df['delta'].rolling(window=7).mean()

# --- PLOTTING ---

# Plot 1: Your Original Overlapping Trends
plt.figure(figsize=(12, 5))
plt.plot(daily_before['day_num'], daily_before[target_col], color='blue', alpha=0.2, label='Daily Before')
plt.plot(daily_after['day_num'], daily_after[target_col], color='orange', alpha=0.2, label='Daily After')
plt.plot(daily_before['day_num'], daily_before[target_col].rolling(7).mean(), color='blue', linewidth=2, label='Trend Before')
plt.plot(daily_after['day_num'], daily_after[target_col].rolling(7).mean(), color='orange', linewidth=2, label='Trend After')
plt.title("Overlapping Trends")
plt.legend()

# Plot 2: The Difference (The "Gap" between the trends)
plt.figure(figsize=(12, 5))

# Fill area to show savings vs increase
plt.fill_between(diff_df['day_num'], diff_df['delta'], 0, where=(diff_df['delta'] < 0), color='green', alpha=0.3, label='Usage Decrease')
plt.fill_between(diff_df['day_num'], diff_df['delta'], 0, where=(diff_df['delta'] > 0), color='red', alpha=0.3, label='Usage Increase')

# Plot the 7-day trend of the difference
plt.plot(diff_df['day_num'], diff_df['delta_smooth'], color='black', linewidth=2, label='7-Day Avg Difference')

plt.axhline(0, color='black', linestyle='--') # Baseline
plt.title(f"Net Difference in Energy Usage (After - Before)")
plt.xlabel("Days Since Period Start")
plt.ylabel(f"Difference in {target_col}")
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Quick Summary
avg_saving = diff_df['delta'].mean()
print(f"Average daily change after {RATE_CHANGE_DATE}: {avg_saving:.2f} {target_col}")