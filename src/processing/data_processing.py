from pyspark.sql import SparkSession
from pyspark.sql.functions import window

class DataProcessing:
    def __init__(self, spark: SparkSession):
        self.spark = spark

    def process_stream(self, raw_data_stream):
        return raw_data_stream \
            .withColumn("minute", window("timestamp", "1 minute")) \
            .withWatermark("timestamp", "1 minute")
