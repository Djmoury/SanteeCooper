
import pandas as pd

df = pd.read_csv("energy_synth.csv.zip")

#Set Variables for each column header
Customer = df["customer_id"]
Energy = df["kWhr"]
Time = df["date_time"]

#Task 1: How many Customers are there
num_customer = Customer.nunique()  #useful function
print(num_customer)
#Answer: 300 Customers ##################################################################################

#Task 2 How many days per customer
Time = pd.to_datetime(Time) #changes time to datetime ***
dates_only = Time.dt.date

data = pd.DataFrame({    #Makes a seperate data sheet for customers and dates only;
    "Customer": Customer,
    "Date": dates_only
})

days_per_customer = data.groupby("Customer")["Date"].nunique()  #Splits data by each customer, looks at the date column,
                                                                # and counts unique dates per customer
print(days_per_customer)

print(df)
#Each customer had 210 days tracked #####################################################################

#Task 3: Total Energy Per Customer
total_energy = Energy.sum()
print("Total energy used by all customers:", total_energy)

energy_per_customer = df.groupby("customer_id")["kWhr"].sum()
print(energy_per_customer)

print(df)


