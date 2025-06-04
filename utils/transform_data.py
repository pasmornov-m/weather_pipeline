from utils.reader import read_from_parquet
from utils.writer import write_to_parquet
from db_utils.spark_schemas import WEATHER_SCHEMA
from pyspark.sql import SparkSession
from pyspark.sql.types import *
import pyspark.sql.functions as F
from datetime import datetime
# import sys

def transform_data(spark, raw_path, processed_path):
    raw_data = read_from_parquet(spark, raw_path)

    df = raw_data \
    .withColumnRenamed("timestamp", "timestamp_utc") \
    .withColumn("timestamp_utc", F.to_timestamp(F.col("timestamp_utc"))) \
    .withColumn("temperature", F.col("temperature").cast(FloatType())) \
    .withColumn("feels_like", F.col("feels_like").cast(FloatType())) \
    .withColumn("pressure", F.col("pressure").cast(IntegerType())) \
    .withColumn("humidity", F.col("humidity").cast(IntegerType())) \
    .withColumn("wind_speed", F.col("wind_speed").cast(FloatType())) \
    .withColumn("wind_deg", F.col("wind_deg").cast(IntegerType())) \
    .withColumn("clouds", F.col("clouds").cast(IntegerType()))

    # df.printSchema()
    # df.show(truncate=False)
    return df


def normalize_raw_data(data):
    return {
        "country": data["country"],
        "city": data["city"],
        "timestamp": data["timestamp"],
        "temperature": float(data["temperature"]),
        "feels_like": float(data["feels_like"]),
        "pressure": int(data["pressure"]),
        "humidity": int(data["humidity"]),
        "weather_main": data["weather_main"],
        "weather_description": data["weather_description"],
        "wind_speed": float(data["wind_speed"]),
        "wind_deg": int(data["wind_deg"]),
        "clouds": int(data["clouds"]),
    }