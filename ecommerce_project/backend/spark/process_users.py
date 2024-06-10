from pyspark.sql import SparkSession

def process_users(spark: SparkSession, users_path: str):
    df = spark.read.json(users_path)
    df.show()
    return df
