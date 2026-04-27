import os
os.environ["JAVA_HOME"] = "/Library/Java/JavaVirtualMachines/temurin-17.jdk/Contents/Home"
import delta_sharing
import pandas as pd
import random

profile_file = "../.venv/config.share"
table_url = "config.share#ccu-delta-share.account_metering.intervals_redacted"

sample = delta_sharing.load_as_pandas(table_url, limit=50000)

unique_customers = sample['meter_base'].unique()


print("Selected customers:", unique_customers)


customer_data = sample[sample['meter_base'].isin(unique_customers)]

print("Rows for 10 customers:", len(customer_data))
print(customer_data.to_string())


#pd.set_option('display.max_columns', None)
#pd.set_option('display.max_rows', None)
#pd.set_option('display.width', None)
#pd.set_option('display.max_colwidth', None)


#print("\nColumn names & types:")
print(sample.dtypes)


#print(sample)
'''

import time
import glob
import pandas as pd
import delta_sharing
from pyspark.sql import SparkSession

profile_file = "config.share"
table_url = "config.share#ccu-delta-share.account_metering.intervals_redacted"

spark = SparkSession.builder \
    .appName("DeltaSharingLoad") \
    .config("spark.jars.packages", "io.delta:delta-sharing-spark_2.12:3.1.0") \
    .getOrCreate()

# Example: sample a manageable chunk for analysis
df = spark.read.format("deltaSharing").load(table_url) \
    .select("KWH", "meter_base", "meter_number")



start = time.time()
count = df.count()
end = time.time()

print(f"Row count: {count}")
print(f"Time taken: {end - start:.2f} seconds")


print(df.count())

import os
os.environ["JAVA_HOME"] = "/Library/Java/JavaVirtualMachines/temurin-17.jdk/Contents/Home"

import time
import pandas as pd
import delta_sharing
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

profile_file = "config.share"
table_url = "config.share#ccu-delta-share.account_metering.intervals_redacted"

spark = SparkSession.builder \
    .appName("DeltaSharingLoad") \
    .config("spark.jars.packages", "io.delta:delta-sharing-spark_2.12:3.1.0") \
    .getOrCreate()

df = spark.read.format("deltaSharing").load(table_url) \
    .select("KWH", "meter_base", "meter_number")

# --- Sequential Sample (50000 rows) ---
start = time.time()
sequential_df = df.limit(50000)
sequential_pd = sequential_df.toPandas()
seq_time = time.time() - start
print(f"Sequential sample time: {seq_time:.2f} seconds")

# --- Random Sample (48 rows at a time, across different offsets) ---
start = time.time()
random_df = df.sample(fraction=0.0001, seed=42).limit(50000)
random_pd = random_df.toPandas()
rand_time = time.time() - start
print(f"Random sample time: {rand_time:.2f} seconds")
'''
