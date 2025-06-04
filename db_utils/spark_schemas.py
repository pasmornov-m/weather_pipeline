from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, DateType, FloatType, TimestampType

WEATHER_SCHEMA = StructType([
    StructField("country", StringType(), True),
    StructField("city", StringType(), True),
    StructField("timestamp_utc", TimestampType(), False),
    StructField("temperature", FloatType(), True),
    StructField("feels_like", FloatType(), True),
    StructField("pressure", IntegerType(), True),
    StructField("humidity", IntegerType(), True),
    StructField("weather_main", StringType(), True),
    StructField("weather_description", StringType(), True),
    StructField("wind_speed", FloatType(), True),
    StructField("wind_deg", IntegerType(), True),
    StructField("clouds", IntegerType(), True),
])

RAW_WEATHER_SCHEMA = StructType([
    StructField("country", StringType(), True),
    StructField("city", StringType(), True),
    StructField("timestamp", StringType(), True),
    StructField("temperature", DoubleType(), True),
    StructField("feels_like", DoubleType(), True),
    StructField("pressure", IntegerType(), True),
    StructField("humidity", IntegerType(), True),
    StructField("weather_main", StringType(), True),
    StructField("weather_description", StringType(), True),
    StructField("wind_speed", DoubleType(), True),
    StructField("wind_deg", IntegerType(), True),
    StructField("clouds", IntegerType(), True),
])