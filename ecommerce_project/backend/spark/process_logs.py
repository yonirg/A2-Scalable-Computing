from pyspark.sql import SparkSession

def process_logs(spark: SparkSession, logs_path: str):
    df = spark.read.text(logs_path)
    df.show()
    return df
