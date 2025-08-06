from minio.error import S3Error
import json
import tempfile
from clients.minio_client import create_minio_client
from config import MINIO_TEMP_BUCKET, OFFSET_FILE


def read_from_parquet(spark, path):
    return spark.read.parquet(path)

def read_from_json(spark, path):
    df = spark.read.json(path)
    if df.isEmpty():
        raise ValueError(f"JSON-файл пуст или отсутствует по пути: {path}")
    return df.first().asDict()

def load_offset_from_minio():
    client = create_minio_client()

    if not client.bucket_exists(MINIO_TEMP_BUCKET):
        print(f"MinIO bucket '{MINIO_TEMP_BUCKET}' не существует")
        return -1

    try:
        client.stat_object(MINIO_TEMP_BUCKET, OFFSET_FILE)
    except S3Error as e:
        if e.code == "NoSuchKey":
            return -1
        else:
            raise e

    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        client.fget_object(MINIO_TEMP_BUCKET, OFFSET_FILE, tmp_file.name)
        tmp_file_path = tmp_file.name

    with open(tmp_file_path, 'r') as f:
        offset_data = json.load(f)

    offset = offset_data.get("offset")
    if offset is None:
        raise ValueError("Offset не найден в JSON")

    return offset
