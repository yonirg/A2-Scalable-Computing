from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum

class BonusSystem:
    def __init__(self, spark: SparkSession):
        self.spark = spark

    def check_bonuses(self, processed_data):
        X = 1000  # Valor hard-coded para bonificação em 10 minutos
        Y = 5000  # Valor hard-coded para bonificação em 6 horas

        bonuses = processed_data \
            .filter(col("event") == "purchase") \
            .withWatermark("timestamp", "6 hours") \
            .groupBy(window(col("timestamp"), "10 minutes", "6 hours")) \
            .agg(sum("price").alias("totalRevenue")) \
            .filter(col("totalRevenue") > X) \
            .filter(col("totalRevenue") > Y)

        # Placeholder for notifying users
        bonuses.writeStream \
            .format("console") \
            .outputMode("update") \
            .start()
