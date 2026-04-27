import os
os.environ["JAVA_HOME"] = "/Library/Java/JavaVirtualMachines/temurin-17.jdk/Contents/Home"

import pandas as pd
import matplotlib.pyplot as plt
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

# -----------------------------
# 1. Spark Session
# -----------------------------
spark = SparkSession.builder \
    .appName("DeltaSharingLoad") \
    .config("spark.jars.packages", "io.delta:delta-sharing-spark_2.12:3.1.0") \
    .config("spark.driver.memory", "8g") \
    .config("spark.executor.memory", "8g") \
    .config("spark.delta.sharing.network.numRetries", "10") \
    .config("spark.delta.sharing.network.maxConnections", "32") \
    .config("spark.delta.sharing.network.timeout", "120") \
    .getOrCreate()

# -----------------------------
# 2. Load & Filter in Spark
# -----------------------------
table_url = "config.share#ccu-delta-share.account_metering.intervals_redacted"

spark_df = spark.read.format("deltaSharing").load(table_url)
'''
# -----------------------------
# 3. Get First Customer & Aggregate in Spark
# -----------------------------
first_meter = spark_df \
    .orderBy("start_datetime") \
    .select("meter_number") \
    .first()["meter_number"]

df = spark_df \
    .filter(F.col("meter_number") == first_meter) \
    .withColumn("hour", F.hour("start_datetime")) \
    .groupBy("hour") \
    .agg(F.avg("kwh").alias("kWhr")) \
    .orderBy("hour") \
    .toPandas()

# -----------------------------
# 4. Plot Average Across All Days
# -----------------------------
plt.plot(df["hour"], df["kWhr"], color='red', linewidth=2)
plt.title(f"Average Hourly Energy Usage\n{first_meter}")
plt.xlabel("Hour of Day")
plt.ylabel("kWhr")
plt.xticks(range(0, 24))
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
'''

# -----------------------------
# 3. Get First Customer & Aggregate by Day in Spark
# -----------------------------
first_meter = spark_df \
    .orderBy("start_datetime") \
    .select("meter_number") \
    .first()["meter_number"]

df = spark_df \
    .filter(F.col("meter_number") == first_meter) \
    .filter(F.col("start_datetime") >= "2025-03-01") \
    .filter(F.col("start_datetime") < "2025-06-01") \
    .withColumn("date", F.to_date("start_datetime")) \
    .groupBy("date") \
    .agg(F.avg("kwh").alias("avg_kWhr")) \
    .orderBy("date") \
    .toPandas()

# -----------------------------
# 4. Plot Daily Average Across the Year
# -----------------------------
'''
df["date"] = pd.to_datetime(df["date"])

plt.figure(figsize=(14, 5))
plt.plot(df["date"], df["avg_kWhr"], color='red', linewidth=1)
plt.title(f"Daily Average Energy Usage\n{first_meter}\n{df['date'].min().date()} to {df['date'].max().date()}")
plt.xlabel("Date")
plt.ylabel("Avg kWhr")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
'''
df["date"] = pd.to_datetime(df["date"])
split_date = pd.Timestamp("2025-04-15")

before = df[df["date"] < split_date]
after = df[df["date"] >= split_date]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 5), sharey=True)

for date, group in before.groupby("date"):
    ax1.plot(group["hour"], group["kWhr"], color='blue', alpha=0.3, linewidth=0.8)
ax1.set_title(f"Before April 15, 2025\n{before['date'].min().date()} to {before['date'].max().date()}")
ax1.set_xlabel("Hour of Day")
ax1.set_ylabel("kWhr")
ax1.set_xticks(range(0, 24))
ax1.grid(True, alpha=0.3)

for date, group in after.groupby("date"):
    ax2.plot(group["hour"], group["kWhr"], color='red', alpha=0.3, linewidth=0.8)
ax2.set_title(f"After April 15, 2025\n{after['date'].min().date()} to {after['date'].max().date()}")
ax2.set_xlabel("Hour of Day")
ax2.set_xticks(range(0, 24))
ax2.grid(True, alpha=0.3)

plt.suptitle(f"Hourly Energy Usage — {first_meter}", fontsize=13)
plt.tight_layout()
plt.show()