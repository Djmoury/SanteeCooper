import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans

#Load the dataset from a zipped CSV file into a pandas dataframe
df = pd.read_csv("energy_synth.csv.zip")
#Convert the date_time column from plain text to actual datetime objects
df["date_time"] = pd.to_datetime(df["date_time"])

#Energy usage in kilowatt hours
target_col = "kWhr"

#The date the energy rate changed
RATE_CHANGE_DATE = "2025-04-15"
rate_date = pd.to_datetime(RATE_CHANGE_DATE)

#Extract just the hour (0-23) from each timestamp into its own column for easy analysis
df["hour"] = df["date_time"].dt.hour

#Gets a list of all unique customer IDs in the dataset
sample = df["customer_id"].unique()

print(f"Total customers in dataset: {df['customer_id'].nunique()}")

#Creates an empty list to store each customer's normalized profile and their ID
profiles = []

#Loop through every customer
for cust in sample:
    #Splits data into Before and After the rate change
    pre  = df[(df["customer_id"] == cust) & (df["date_time"] <  rate_date)]
    post = df[(df["customer_id"] == cust) & (df["date_time"] >= rate_date)]

    #Averages the kWhr usage by hour for the pre and post periods
    pre_mean  = pre.groupby("hour")[target_col].mean().reindex(range(24), fill_value=0)
    post_mean = post.groupby("hour")[target_col].mean().reindex(range(24), fill_value=0)

    diff = post_mean - pre_mean

    #Normalize the difference so all customers are on the same scale regardless of how much energy they use overall
    #This is because the clustering is about When not How Much
    norm_diff = (diff - diff.mean()) / diff.std()
    #Stores the normalized profile and customer ID
    profiles.append(norm_diff.values)

#Converts the list of profiles into a numpy array for graphing later
profile_matrix = np.array(profiles)

################## Actual K means Clustering ######################
#Used 2 based on Feedback
K = 2
#K means randomly places cluster centers, Use random_state to keep it the same everytime
#any number will work; just chose 50 at random.
kmeans = KMeans(n_clusters=K, random_state=50)
#fit is locating where to best place the 2 centroids; predict assigns each customer
#according to which centroid they are closest to. (0 or 1)
labels = kmeans.fit_predict(profile_matrix)

################ Actual Plotting ################
cluster_colors = ["blue", "red"]

fig, ax = plt.subplots(figsize=(14, 6))

#Plots every customer's normalized profile as a (faint) line
for i, profile in enumerate(profile_matrix):
    ax.plot(range(24), profile,
            color=cluster_colors[labels[i]],
            alpha=0.15,
            linewidth=0.8)

#Overlays the cluster centroid lines (Bold)
for k in range(K):
    centroid = profile_matrix[labels == k].mean(axis=0)
    count = (labels == k).sum()
    ax.plot(range(24), centroid,
            color=cluster_colors[k],
            linewidth=3,
            label=f"Cluster {k+1} centroid ({count} customers)")

ax.axhline(0, color="black", linewidth=1, linestyle=":")
ax.set_title(f"{len(sample)} Customers Normalized Hourly Difference (Post - Pre)\nwith K=2 Cluster Centroids")
ax.set_xlabel("Hour of Day")
ax.set_ylabel("Normalized Difference")
ax.set_xticks(range(0, 24))
ax.grid(True, alpha=0.3)
ax.legend()

ax.set_xlim(0, 23)
plt.tight_layout()
plt.show()