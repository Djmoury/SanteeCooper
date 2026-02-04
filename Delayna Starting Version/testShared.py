import pandas as pd

df = pd.read_csv("energy_synth.csv")

customer = df["customer_id"]
energy = df["kWhr"]
time= df["date_time"]

print (df.head())
#Task 1 - Unique customers
num_customers = customer.nunique()
print(num_customers)
#300 customers

#Task 2 - Days per customer
Time= pd.to_datetime(time)
dates = Time.dt.date

data = pd.DataFrame({
    "Customer": customer,
    "date": dates

})

days_per_customer= data.groupby("Customer")["date"].nunique()
print(days_per_customer)
print(df)

#210 dates tracked

#Task 3
total_energy = energy.sum()
print("used by all customers", total_energy)
energy_per_customer = df.groupby("customer_id")["kWhr"].sum()
print(energy_per_customer)



