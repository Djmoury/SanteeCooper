
############################# V2 ###################################

import pandas as pd #Read Data
import numpy as np #Create Graphs

df = pd.read_csv("../Indentifying Trends Code/energy_synth.csv.zip")
df["date_time"] = pd.to_datetime(df["date_time"]) #Converts strings into date_time object so it can read as one

################# Split Data Into Before/After ####################

RATE_CHANGE_DATE = "2025-04-15"
rate_date = pd.to_datetime(RATE_CHANGE_DATE) #Same function as Line 8

df_before = df[df["date_time"] < rate_date] #Outer df[] gives all rows, where the condition inside is true
                                            #Inside df chooses only that column and compares to the day rates changed
df_after  = df[df["date_time"] >= rate_date] #Day-Of is included in the "After" category

###################### Metrics Class ###########################

class EnergyMetrics:
    def __init__(self, df): # __init__ runs these functions automatically when an object is made
        self.df = df #self stores the data inside the object so its not forgotten

    def total_energy(self):
        return self.df["kWhr"].sum()

    def average_energy(self):
        return self.df["kWhr"].mean()

    def by_month(self):
        return (
            self.df
            .groupby(self.df["date_time"].dt.month)["kWhr"] #Groups all rows that occured on the same MONTH together and uses only the energy column
            .agg(["sum", "mean"]) #Computes sum and mean at once
        )

    def by_day(self):
        return (
            self.df
            .groupby(self.df["date_time"].dt.date)["kWhr"] #Groups all rows that occured on the same DAY
            .agg(["sum", "mean"])
        )
    # I somehow need to make this part turn into weekdays instead of everysingle day covered in the data Maybe these:
    # weekday_before = metrics_before.by_weekday()
    # weekday_after = metrics_after.by_weekday()

    def by_hour(self):
        return (
            self.df
            .groupby(self.df["date_time"].dt.hour)["kWhr"] #Groups al rows that occured in the same HOUR
            .agg(["sum", "mean"])
        )
# This class computes metrics for whatever dataset I give it Before/After; It's easily repeatable

##################### Create Objects #####################

metrics_before = EnergyMetrics(df_before)
metrics_after  = EnergyMetrics(df_after)

# I've created a class that computes metrics for a data set
# I then created 2 objects, one before the rate change and one after
# Need help with making the graphs









