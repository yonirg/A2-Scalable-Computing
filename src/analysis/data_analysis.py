from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, sum, countDistinct

class DataAnalysis:
    def __init__(self, spark: SparkSession):
        self.spark = spark

    def analyze_stream(self, processed_data):
        purchases_per_minute = processed_data \
            .filter(col("event") == "purchase") \
            .groupBy("minute") \
            .agg(count("productId").alias("productsBought"), sum("price").alias("totalRevenue"))

        unique_users_per_product = processed_data \
            .groupBy("productId", "minute") \
            .agg(countDistinct("userId").alias("uniqueViewers"))

        purchases_per_minute.writeStream \
            .format("console") \
            .outputMode("update") \
            .start()

        unique_users_per_product.writeStream \
            .format("console") \
            .outputMode("update") \
            .start()
