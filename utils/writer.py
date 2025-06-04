from clients.minio_client import create_minio_client
from config import MINIO_TEMP_BUCKET, OFFSET_FILE
import json
import tempfile
import os
from pyspark.sql import DataFrame


def write_to_json(spark, data, path):
    df = spark.createDataFrame(data)
    df.write.mode("overwrite").json(path)

def write_to_parquet(spark, data, path, mode="overwrite"):
    if isinstance(data, DataFrame):
        df = data
    else:
        df = spark.createDataFrame(data)
        
    df.write.mode(mode).parquet(path)

def save_offset_to_minio(offset):
    if offset is None:
        raise ValueError("Offset is not available")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode='w') as tmp_file:
        json.dump({'offset': offset}, tmp_file, indent=2)
        tmp_file_path = tmp_file.name

    client = create_minio_client()

    if not client.bucket_exists(MINIO_TEMP_BUCKET):
        client.make_bucket(MINIO_TEMP_BUCKET)

    client.fput_object(
        bucket_name=MINIO_TEMP_BUCKET,
        object_name=OFFSET_FILE,
        file_path=tmp_file_path,
        content_type='application/json'
    )

    os.remove(tmp_file_path)

def write_to_postgres(df, table, properties):
    df.write.jdbc(
        url=properties['url'],
        table=table,
        mode='append',
        properties={
            "user": properties['user'],
            "password": properties['password'],
            "driver": properties['driver']
        }
    )