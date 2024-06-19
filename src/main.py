from pyspark.sql import SparkSession
from ingestion.data_ingestion import DataIngestion
from processing.data_processing import DataProcessing
from analysis.data_analysis import DataAnalysis
from bonus.bonus_system import BonusSystem
from price_monitor.price_monitor import PriceMonitor
import os

def main():
    spark = SparkSession.builder \
        .appName("Data Processing Pipeline") \
        .master("local[*]") \
        .getOrCreate()

    ingestion = DataIngestion(spark)
    processing = DataProcessing(spark)
    analysis = DataAnalysis(spark)
    bonus_system = BonusSystem(spark)
    price_monitor = PriceMonitor(spark)

    raw_data_stream = ingestion.read_stream()
    processed_data = processing.process_stream(raw_data_stream)
    analysis.analyze_stream(processed_data)
    bonus_system.check_bonuses(processed_data)
    price_monitor.monitor_prices()

    spark.streams.awaitAnyTermination()

if __name__ == "__main__":
    main()
