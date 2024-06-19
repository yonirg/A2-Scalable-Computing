from pyspark.sql import SparkSession
from pyspark.sql.types import StructType

class DataIngestion:
    def __init__(self, spark: SparkSession):
        self.spark = spark

    def read_stream(self):
        schema = StructType() \
            .add("event", "string") \
            .add("timestamp", "timestamp") \
            .add("userId", "string") \
            .add("productId", "string") \
            .add("price", "double")

        return self.spark.readStream \
            .format("json") \
            .schema(schema) \
            .load("path/to/your/data/source")
