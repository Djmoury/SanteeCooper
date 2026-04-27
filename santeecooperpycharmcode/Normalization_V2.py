import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans

df = pd.read_csv("energy_synth.csv.zip")
df["date_time"] = pd.to_datetime(df["date_time"])

target_col = "kWhr"

RATE_CHANGE_DATE = "2025-04-15"
rate_date = pd.to_datetime(RATE_CHANGE_DATE)
df["hour"] = df["date_time"].dt.hour

sample = df["customer_id"].unique()


profiles = []
valid_customers = []

for cust in sample:
    pre  = df[(df["customer_id"] == cust) & (df["date_time"] <  rate_date)]
    post = df[(df["customer_id"] == cust) & (df["date_time"] >= rate_date)]

    if len(pre) == 0 or len(post) == 0:
        continue

    pre_mean  = pre.groupby("hour")[target_col].mean().reindex(range(24), fill_value=0)
    post_mean = post.groupby("hour")[target_col].mean().reindex(range(24), fill_value=0)

    diff = post_mean - pre_mean

    if diff.std() < 1e-6:
        continue

    norm_diff = (diff - diff.mean()) / diff.std()
    profiles.append(norm_diff.values)
    valid_customers.append(cust)

profile_matrix = np.array(profiles)  # shape: (n_customers, 24)


K = 5
kmeans = KMeans(n_clusters=K, random_state=42, n_init=10)
labels = kmeans.fit_predict(profile_matrix)


colors = ["blue", "red", "green", "orange", "purple"]

y_min = profile_matrix.min()
y_max = profile_matrix.max()

for k in range(K):
    fig, ax = plt.subplots(figsize=(12, 5))

    cluster_profiles = profile_matrix[labels == k]
    mean_profile = cluster_profiles.mean(axis=0)

    ax.plot(range(24), mean_profile, color=colors[k], linewidth=2.5)
    ax.axhline(0, color="black", linewidth=1, linestyle=":")

    ax.set_title(f"Cluster {k+1} ({len(cluster_profiles)} customers)")
    ax.set_xlabel("Hour of Day")
    ax.set_ylabel("Normalized Difference")
    ax.set_xticks(range(0, 24))
    ax.set_ylim(y_min, y_max)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()