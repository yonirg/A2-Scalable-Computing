from pyspark.sql import SparkSession

def process_transactions(spark: SparkSession, transactions_path: str):
    df = spark.read.json(transactions_path)
    df.show()
    return df
