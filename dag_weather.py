from airflow import DAG
from airflow.operators.python import PythonOperator
# from airflow.providers.postgres.hooks.postgres import PostgresHook
# from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime, timedelta
# import os, json
from confluent_kafka import Consumer
from utils.writer import save_offset_to_minio
from utils.reader import load_offset_from_minio
from utils.fetch_data import fetch_kafka_data
from utils.transform_data import transform_data
from clients.spark_client import create_spark_session
from db_utils.check_gp import create_db_schema_table
from config import GREENPLUM_CONN_ID, MINIO_RAW_BUCKET


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(seconds=60)
}

dag = DAG('weather_batch_pipeline',
          default_args=default_args,
          schedule_interval='@hourly',
          catchup=False)


def task_load_offset(**context):
    offset = load_offset_from_minio()
    context['ti'].xcom_push(key='offset', value=offset)

def task_fetch_kafka_data(**context):
    offset_data = context['ti'].xcom_pull(key='offset')
    last_offset = offset_data['offset']

    spark = create_spark_session()
    last_offset = fetch_kafka_data(spark, MINIO_RAW_BUCKET, last_offset)
    spark.stop()

    context['ti'].xcom_push(key='offset', value=last_offset)

def task_transform_data(**context):
    transform_data_path = transform_data(spark, bucket_raw, bucket_processed)
    context['ti'].xcom_push(key='transform_data_path', value=transform_data_path)


def load_to_greenplum(**context):
    transform_data_path = context['ti'].xcom_pull(key='transform_data_path')
    df = pd.read_parquet(transform_data_path)

    pg_hook = PostgresHook(postgres_conn_id=GREENPLUM_CONN_ID)
    conn = pg_hook.get_conn()
    cursor = conn.cursor()

    for _, row in df.iterrows():
        cursor.execute(
            "INSERT INTO fact_weather(datetime, temperature) VALUES (%s, %s)",
            (row['datetime'], row['temperature_C'])
        )

    conn.commit()

def save_offset(**context):
    offset = context['ti'].xcom_pull(key='offset')
    save_offset_to_minio(offset)


check_task = PythonOperator(task_id='check_database_and_table', python_callable=create_db_schema_table)
fetch_task = PythonOperator(task_id='fetch_kafka_data', python_callable=fetch_kafka_data, provide_context=True, dag=dag)
transform_task = PythonOperator(task_id='transform_data', python_callable=transform_data, provide_context=True, dag=dag)
load_gp_task = PythonOperator(task_id='load_to_greenplum', python_callable=load_to_greenplum, provide_context=True, dag=dag)
save_offset_task = PythonOperator(task_id='save_offset', python_callable=save_offset, provide_context=True, dag=dag)


fetch_task >> transform_task >> load_gp_task >> save_offset_task
