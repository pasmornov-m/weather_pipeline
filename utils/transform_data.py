from utils.reader import read_from_json
from utils.link_to_s3 import link_to_s3
from pyspark.sql import SparkSession
import sys

def transform_data(spark, bucket_raw, bucket_processed):
    raw_path = link_to_s3(bucket_raw)
    raw_data = read_from_json(spark, raw_path)



    return transform_data_path


if __name__ == "__main__":
    spark = SparkSession.builder.appName("transform_data").getOrCreate()
    bucket_raw = sys.argv[2]
    bucket_processed = sys.argv[2]
    transform_data(spark, bucket_raw, bucket_processed)
    spark.stop()