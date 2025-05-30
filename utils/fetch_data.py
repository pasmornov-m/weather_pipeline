import requests
from datetime import datetime
import json
from clients.kafka_client import create_kafka_consumer
from clients.spark_client import create_spark_session
from utils.writer import write_to_json
from utils.link_to_s3 import link_to_s3
from config import KAFKA_TOPIC, MINIO_RAW_BUCKET



def fetch_weather(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        result = {
            "country": data["sys"]["country"],
            "city": data.get("name"),
            "timestamp": datetime.utcfromtimestamp(data["dt"]).isoformat(),
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "pressure": data["main"]["pressure"],
            "humidity": data["main"]["humidity"],
            "weather_main": data["weather"][0]["main"],
            "weather_description": data["weather"][0]["description"],
            "wind_speed": data["wind"]["speed"],
            "wind_deg": data["wind"]["deg"],
            "clouds": data["clouds"]["all"]
        }
        return result
    except Exception as e:
        print(f"[{datetime.utcnow().isoformat()}] Error fetching data: {e}")
        return None


def fetch_kafka_data(last_offset):
    consumer = create_kafka_consumer()
    consumer.subscribe([KAFKA_TOPIC])

    records = []
    timeout_ms = 3000
    while True:
        msg = consumer.poll(timeout_ms / 1000)
        if msg is None:
            break
        if msg.offset() <= last_offset:
            continue
        data = json.loads(msg.value().decode('utf-8'))
        records.append(data)
        last_offset = msg.offset()
    consumer.close()

    print(records)

    # spark = create_spark_session()
    # path = link_to_s3(MINIO_RAW_BUCKET)
    # write_to_json(spark, records, path)

    return last_offset