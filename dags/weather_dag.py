from utils.writer import save_offset_to_minio, write_to_parquet, write_to_postgres
from utils.reader import load_offset_from_minio, read_from_parquet
from utils.fetch_data import fetch_kafka_data
from utils.transform_data import transform_data
from clients.spark_client import create_spark_session
from db_utils.check_gp import create_db_schema_table
from clients.postgres_client import get_postgres_properties
from config import MINIO_RAW_PATH, MINIO_PROCESSED_PATH, DB_TABLE

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta


default_args = {
    'owner': 'maxp',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'retries': 1,
    "retry_delay": timedelta(minutes=1)
}

dag = DAG(
    dag_id = "weather_api",
    default_args=default_args,
    schedule="@hourly",
    catchup=False,
    tags=['etl'],
)

def fetch_raw_kafka_data(**kwargs):
    raw_path=kwargs['raw_path']

    spark = create_spark_session()
    offset = load_offset_from_minio()
    print(f"current offset: {offset}")
    last_offset = fetch_kafka_data(spark, raw_path, offset)
    print("kafka data fetched")
    save_offset_to_minio(last_offset)
    print(f"last offset: {last_offset}")
    spark.stop()

def transform_raw_data(**kwargs):
    raw_path = kwargs['raw_path']
    processed_path = kwargs['processed_path']

    spark = create_spark_session()
    df_transform = transform_data(spark, raw_path, processed_path)
    write_to_parquet(spark, df_transform, processed_path)
    print("Data transformed")
    spark.stop()

def write_data_to_gp(**kwargs):
    table_name = kwargs['table_name']
    processed_path = kwargs['processed_path']

    spark = create_spark_session()
    df_transform_pq = read_from_parquet(spark, processed_path)
    properties = get_postgres_properties()
    write_to_postgres(df_transform_pq, table_name, properties)
    print("Data saved to greenplum")
    spark.stop()


create_tables_task = PythonOperator(
    task_id='create_tables',
    python_callable=create_db_schema_table,
    dag=dag
)

fetch_raw_kafka_data_task = PythonOperator(
    task_id='fetch_raw_kafka_data',
    python_callable=fetch_raw_kafka_data,
    op_kwargs={
        'raw_path': MINIO_RAW_PATH
    },
    dag=dag
)

transform_data_task = PythonOperator(
    task_id='transform_raw_data',
    python_callable=transform_raw_data,
    op_kwargs={
        'raw_path': MINIO_RAW_PATH,
        'processed_path': MINIO_PROCESSED_PATH
    },
    dag=dag
)

write_data_to_gp_task = PythonOperator(
    task_id='write_to_gp',
    python_callable=write_data_to_gp,
    op_kwargs={
        'table_name': DB_TABLE,
        'processed_path': MINIO_PROCESSED_PATH
    },
    dag=dag
)

create_tables_task >> fetch_raw_kafka_data_task >> transform_data_task >> write_data_to_gp_task