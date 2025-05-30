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
MINIO_PROCESSED_BUCKET = "processed-data"
MINIO_TEMP_BUCKET = 'temp'
OFFSET_FILE = "offset_json/weather_offset.json"

# POSTGRES
# POSTGRES_USER = os.getenv("POSTGRES_USER")
# POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
# POSTGRES_URL = "jdbc:postgresql://db:5432/orient_data"


# SPARK
SPARK_APP_NAME = "Weather"
SPARK_MASTER = "spark://spark:7077"


# KAFKA
KAFKA_TOPIC = 'weather_raw'
KAFKA_BOOTSTRAP_SERVERS = 'broker:29092'
# KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'
KAFKA_GROUP_ID = 'airflow_batch_group'
KAFKA_FETCH_INTERVAL = 1800


# GREENPLUM
GREENPLUM_CONN_ID = 'greenplum_default'
