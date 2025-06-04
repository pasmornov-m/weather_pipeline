import json
from clients.kafka_client import create_kafka_consumer
from utils.writer import write_to_parquet
from utils.transform_data import normalize_raw_data
from config import KAFKA_TOPIC
from db_utils.spark_schemas import RAW_WEATHER_SCHEMA
# from pyspark.sql import SparkSession
# import sys


def fetch_kafka_data(spark, raw_path, last_offset):
    consumer = create_kafka_consumer()
    consumer.subscribe([KAFKA_TOPIC])

    records = []
    timeout_ms = 3000
    while True:
        msg = consumer.poll(timeout=timeout_ms/1000)

        if msg is None:
            break
        if msg.error():
            print(f"[Kafka error] {msg.error()}")
            break

        current_offset = msg.offset()
        if current_offset <= last_offset:
            continue

        try:
            data = json.loads(msg.value().decode('utf-8'))
        except Exception as e:
            print(f"[ERROR] Cannot decode/parse message at offset {current_offset}: {e}")
            continue

        records.append(data)
        last_offset = current_offset
    consumer.close()

    print(records)

    normalized_records = [normalize_raw_data(r) for r in records]
    df_records = spark.createDataFrame(normalized_records, schema=RAW_WEATHER_SCHEMA)

    write_to_parquet(spark, df_records, raw_path, mode="overwrite")

    return last_offset


# if __name__ == "__main__":
#     spark = SparkSession.builder.appName("fetch_kafka_data").getOrCreate()
#     bucket_raw = sys.argv[1]
#     last_offset = int(sys.argv[2])
#     fetch_kafka_data(spark, bucket_raw, last_offset)
#     spark.stop()