from pyspark.sql import SparkSession

def get_spark_session(app_name: str = "EcommerceDataProcessing"):
    return SparkSession.builder         .appName(app_name)         .config("spark.some.config.option", "some-value")         .getOrCreate()
