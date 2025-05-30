from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta
import os, json
from confluent_kafka import Consumer
from utils.writer import save_offset_to_minio
from utils.reader import load_offset_from_minio
from utils.fetch_data import fetch_kafka_data
from utils.transform_data import transform_data

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

    last_offset, raw_path = fetch_kafka_data(last_offset)
    
    context['ti'].xcom_push(key='raw_path', value=raw_path)
    context['ti'].xcom_push(key='offset', value=last_offset)

def task_transform_data(**context):
    raw_path = context['ti'].xcom_pull(key='raw_path')
    transform_data_path = transform_data(raw_path)
    

    context['ti'].xcom_push(key='transform_data_path', value=transform_data_path)

# Step 4: Upload to S3
def upload_to_s3(**context):
    file_path = context['ti'].xcom_pull(key='transform_data_path')
    s3_key = f"{S3_PREFIX}/{datetime.now().strftime('%Y/%m/%d/%H')}/data.parquet"
    s3 = boto3.client('s3')
    s3.upload_file(file_path, S3_BUCKET, s3_key)
    return s3_key

# Step 5: Load to Greenplum
def load_to_greenplum(**context):
    file_path = context['ti'].xcom_pull(key='file_path')
    df = pd.read_parquet(file_path)

    pg_hook = PostgresHook(postgres_conn_id=GREENPLUM_CONN_ID)
    conn = pg_hook.get_conn()
    cursor = conn.cursor()

    for _, row in df.iterrows():
        cursor.execute(
            "INSERT INTO fact_weather(datetime, temperature) VALUES (%s, %s)",
            (row['datetime'], row['temperature_C'])
        )

    conn.commit()

# Step 6: Save offset
def save_offset(**context):
    offset = context['ti'].xcom_pull(key='offset')
    save_offset_to_minio(offset)

# DAG tasks
fetch_task = PythonOperator(task_id='fetch_kafka_data', python_callable=fetch_kafka_data, provide_context=True, dag=dag)
transform_task = PythonOperator(task_id='transform_data', python_callable=transform_data, provide_context=True, dag=dag)
upload_task = PythonOperator(task_id='upload_to_s3', python_callable=upload_to_s3, provide_context=True, dag=dag)
load_gp_task = PythonOperator(task_id='load_to_greenplum', python_callable=load_to_greenplum, provide_context=True, dag=dag)
save_offset_task = PythonOperator(task_id='save_offset', python_callable=save_offset, provide_context=True, dag=dag)

# Dependencies
fetch_task >> transform_task >> upload_task >> load_gp_task >> save_offset_task
