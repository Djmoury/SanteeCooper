import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("energy_synth.csv")
df["date_time"] = pd.to_datetime(df["date_time"])

# Min Energy
minEnergy = (
    df
    .groupby(df["date_time"].dt.to_period("M"))["kWhr"]#Grouping by Month, then includes all energy points
    .min() # min function of the energy points for each month
)
minEnergy.index = minEnergy.index.to_timestamp() #makes the to_period("M") function work because it makes it view the numbers for month as the group M
# Plot
plt.figure()
plt.plot(minEnergy.index, minEnergy.values)
plt.xlabel("Time")
plt.ylabel("Minimum Energy (kWhr)")
plt.title("Minimum Energy Across All Customers per Month")
plt.show()

# Max energy
maxEnergy = (
    df
    .groupby(df["date_time"].dt.to_period("M"))["kWhr"] #Grouping by Month, then includes all energy points
    .max() # max function of energy points for each month
    #Can also do per customer, graph would be too cluttered to include all
)
maxEnergy.index = maxEnergy.index.to_timestamp()

# Plot
plt.figure()
plt.plot(maxEnergy.index, maxEnergy.values)
plt.xlabel("Time")
plt.ylabel("Max Energy (kWhr)")
plt.title("Max Energy Across All Customers per Month")
plt.show()


monthlyAvg = (
    df
    .groupby(df["date_time"].dt.to_period("M"))["kWhr"]
    .mean()
)
monthlyAvg.index = monthlyAvg.index.to_timestamp()
plt.figure()
plt.plot(monthlyAvg.index, monthlyAvg.values)
plt.xlabel("Month")
plt.ylabel("Average Energy (kWhr)")
plt.title("Average Energy per Month Across All Customers")
plt.show()

monthlyStd = (
    df
    .groupby(df["date_time"].dt.to_period("M"))["kWhr"]
    .std()
)
monthlyStd.index = monthlyStd.index.to_timestamp()
plt.figure()
plt.plot(monthlyStd.index, monthlyStd.values)
plt.xlabel("Month")
plt.ylabel("Standard Deviation Energy (kWhr)")
plt.title("Standard Deviation Energy per Month Across All Customers")
plt.show()






monthlyStats = df.groupby(df["date_time"].dt.to_period("M"))["kWhr"].agg(['min', 'max', 'mean', 'std'])
monthlyStats.index = monthlyStats.index.to_timestamp()


plt.figure()

plt.plot(monthlyStats.index, monthlyStats['min'], label='Min Energy', color='blue', linestyle='-')
plt.plot(monthlyStats.index, monthlyStats['max'], label='Max Energy', color='red', linestyle='--')
plt.plot(monthlyStats.index, monthlyStats['mean'], label='Average Energy', color='green', linestyle='-.')
plt.plot(monthlyStats.index, monthlyStats['std'], label='Std Dev Energy', color='purple', linestyle=':')


plt.xlabel("Month")
plt.ylabel("Energy (kWhr)")
plt.title("Monthly Energy Stats Across All Customers")
plt.legend()
plt.grid(True)


plt.show()