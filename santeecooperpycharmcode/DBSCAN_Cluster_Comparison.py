import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import DBSCAN

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

#Creates an empty list to store each customer's normalized profile and their ID
profiles = []

#Loop through every customer
for cust in sample:
    #Splits data into Before and After the rate change
    pre  = df[(df["customer_id"] == cust) & (df["date_time"] <  rate_date)]
    post = df[(df["customer_id"] == cust) & (df["date_time"] >= rate_date)]

    #Averages the kWhr usage by hour for the pre and post periods
    pre_mean  = pre.groupby("hour")[target_col].mean()
    post_mean = post.groupby("hour")[target_col].mean()

    diff = post_mean - pre_mean

    #Normalize the difference so all customers are on the same scale
    #focusing on the SHAPE of behavior change, not the magnitude of energy usage
    norm_diff = (diff - diff.mean()) / diff.std()
    #Stores the normalized profile and customer ID
    profiles.append(norm_diff.values)

#Converts the list of profiles into a numpy array for graphing later
profile_matrix = np.array(profiles)

############# Actual DBSCAN Clustering ##############
# eps = maximum distance between two points to be considered neighbors (radius)
# min_samples = minimum number of points to form a dense region (cluster); Chose 5 needed
# DBSCAN assigns -1 to outliers that don't belong to any cluster
dbscan = DBSCAN(eps=4.0, min_samples=2)
labels = dbscan.fit_predict(profile_matrix)

# Find unique cluster labels (-1 means outlier)
unique_labels = sorted(set(labels))
#Finds how many clusters besides -1
n_clusters = len([l for l in unique_labels if l != -1])
#Finds how many outliers
n_outliers = (labels == -1).sum()

print(f"Clusters found: {n_clusters}")
print(f"Outliers found: {n_outliers}")

################ Actual Plotting ################
colors = plt.cm.tab10.colors
outlier_color = "grey"

fig, ax = plt.subplots(figsize=(14, 6))

#Plots every customer's normalized profile as a (faint) line
#Outliers (label = -1) are plotted in grey
for i, profile in enumerate(profile_matrix):
    color = outlier_color if labels[i] == -1 else colors[labels[i] % len(colors)]
    ax.plot(range(24), profile,
            color=color,
            alpha=0.15,
            linewidth=0.8)

#Overlays the cluster centroid lines (Bold)
#Outliers are not given a centroid since they don't belong to a cluster
for k in unique_labels:
    if k == -1:
        #Plots a grey label for outliers but no centroid line
        ax.plot([], [], color=outlier_color, linewidth=3, label=f"Outliers ({n_outliers} customers)")
        continue

    centroid = profile_matrix[labels == k].mean(axis=0)
    count = (labels == k).sum()
    ax.plot(range(24), centroid,
            color=colors[k % len(colors)],
            linewidth=3,
            label=f"Cluster {k+1} centroid ({count} customers)")


ax.axhline(0, color="black", linewidth=1, linestyle=":")
ax.set_title(f"{len(sample)} Customers — DBSCAN Clustering\nNormalized Hourly Difference (Post - Pre)")
ax.set_xlabel("Hour of Day")
ax.set_ylabel("Normalized Difference")
ax.set_xticks(range(0, 24))
ax.set_xlim(0, 23)
ax.grid(True, alpha=0.3)
ax.legend()

plt.tight_layout()
plt.show()