from dotenv import load_dotenv
import os

load_dotenv()

# API
API_KEY = os.getenv("OPENWEATHER_API")


# MINIO
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
MINIO_ENDPOINT = "minio:9000"
# MINIO_ENDPOINT = "localhost:9000"
MINIO_RAW_BUCKET='raw-weather'
MINIO_RAW_PATH=f"s3a://{MINIO_RAW_BUCKET}/kafka_data/"
MINIO_PROCESSED_BUCKET = "processed-data"
MINIO_PROCESSED_PATH=f"s3a://{MINIO_PROCESSED_BUCKET}/transformed_data/"
MINIO_TEMP_BUCKET = 'temp'
OFFSET_FILE = "offset_json/weather_offset.json"

# SPARK
SPARK_APP_NAME = "Weather"
SPARK_MASTER = "local[*]"
# SPARK_JARS_PATH = [
#         "/home/maxp/Work/weather_pipeline/spark_jars/hadoop-aws-3.3.4.jar",
#         "/home/maxp/Work/weather_pipeline/spark_jars/aws-java-sdk-bundle-1.12.262.jar",
#         "/home/maxp/Work/weather_pipeline/spark_jars/postgresql-42.7.5.jar",
#         "/home/maxp/Work/weather_pipeline/spark_jars/wildfly-openssl-1.0.7.Final.jar",
#         "/home/maxp/Work/weather_pipeline/spark_jars/checker-qual-3.48.3.jar"
#     ]

SPARK_JARS_PATH = [
        "/opt/spark/spark_jars/hadoop-aws-3.3.4.jar",
        "/opt/spark/spark_jars/aws-java-sdk-bundle-1.12.262.jar",
        "/opt/spark/spark_jars/postgresql-42.7.5.jar",
        "/opt/spark/spark_jars/wildfly-openssl-1.0.7.Final.jar",
        "/opt/spark/spark_jars/checker-qual-3.48.3.jar"
    ]


# KAFKA
KAFKA_TOPIC = 'weather_raw'
KAFKA_BOOTSTRAP_SERVERS = 'broker:29092'
# KAFKA_BOOTSTRAP_SERVERS_LOCAL = 'localhost:9092'
KAFKA_BOOTSTRAP_SERVERS_LOCAL = 'broker:29092'
KAFKA_GROUP_ID = 'airflow_batch_group'
KAFKA_FETCH_INTERVAL = 600


# GREENPLUM
GREENPLUM_CONN_ID = 'greenplum_default'
DB_NAME = 'weather'
WEATHER_TABLE_NAME = 'fact_openweather_observations'
DB_TABLE = f"{DB_NAME}.{WEATHER_TABLE_NAME}"
GP_USER = os.getenv("GP_USER")
GP_PASSWORD = os.getenv("GP_PASSWORD")
GP_HOST = 'greenplum'
# GP_HOST = 'localhost'
GP_PORT = '5432'
GP_URL = f"jdbc:postgresql://{GP_HOST}:{GP_PORT}/{DB_NAME}"
