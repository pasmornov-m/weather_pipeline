from pyspark.sql import SparkSession
from config import SPARK_APP_NAME, SPARK_MASTER, SPARK_JARS_PATH, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_ENDPOINT


def create_spark_session(app_name=SPARK_APP_NAME):
    return SparkSession.builder \
    .appName(app_name) \
    .master(SPARK_MASTER) \
    .config("spark.hadoop.fs.s3a.endpoint", MINIO_ENDPOINT) \
    .config("spark.hadoop.fs.s3a.access.key", MINIO_ACCESS_KEY) \
    .config("spark.hadoop.fs.s3a.secret.key", MINIO_SECRET_KEY) \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false") \
    .config("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider") \
    .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
    .config("spark.jars", ",".join(SPARK_JARS_PATH)) \
    .getOrCreate()
