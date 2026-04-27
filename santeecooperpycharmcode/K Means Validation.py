import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

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

profile_matrix = np.array(profiles)

# Elbow Method
inertias = []
K_range = range(2, 11)

for k in K_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(profile_matrix)
    inertias.append(km.inertia_)

plt.figure(figsize=(8, 4))
plt.plot(K_range, inertias, marker='o')
plt.title("Elbow Method")
plt.xlabel("Number of Clusters (K)")
plt.ylabel("Inertia")
plt.xticks(K_range)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

#Silhouette Scores
print("Silhouette Scores:")
for k in K_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels_ = km.fit_predict(profile_matrix)
    score = silhouette_score(profile_matrix, labels_)
    print(f"  K={k}  silhouette={score:.4f}")

#Used to determine how many clusters we would relaistically need.
#The curve was gradual the whole way with no sharp bend,
#which just means the data doesn't have super
#distinct natural groupings

#For now continue with k = 5 but can be used later with real data