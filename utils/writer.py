from clients import minio_client
from config import MINIO_TEMP_BUCKET, OFFSET_FILE
import json
import tempfile
import os

def write_to_json(spark, data, path):
    df = spark.createDataFrame(data)
    df.write.mode("overwrite").json(path)

def write_to_parquet(df, path):
    df.write.mode("overwrite").parquet(path)

def save_offset_to_minio(offset):
    if offset is None:
        raise ValueError("Offset is not available")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode='w') as tmp_file:
        json.dump({'offset': offset}, tmp_file, indent=2)
        tmp_file_path = tmp_file.name

    client = minio_client()

    if not client.bucket_exists(MINIO_TEMP_BUCKET):
        client.make_bucket(MINIO_TEMP_BUCKET)

    client.fput_object(
        bucket_name=MINIO_TEMP_BUCKET,
        object_name=OFFSET_FILE,
        file_path=tmp_file_path,
        content_type='application/json'
    )

    os.remove(tmp_file_path)

