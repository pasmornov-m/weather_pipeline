import time
from datetime import datetime
from config import API_KEY, KAFKA_TOPIC, KAFKA_FETCH_INTERVAL
from clients.kafka_client import create_kafka_producer
import requests

CITY = 'Moscow'
COUNTRY = 'ru'
url = f'http://api.openweathermap.org/data/2.5/weather?q={CITY},{COUNTRY}&APPID={API_KEY}'

producer = create_kafka_producer()

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

def main():
    print(f"Starting weather producer, interval={KAFKA_FETCH_INTERVAL}s")
    try:
        while True:
            weather = fetch_weather(url)
            if weather:
                future = producer.send(KAFKA_TOPIC, weather)
                try:
                    record_metadata = future.get(timeout=10)
                    print(f"[{datetime.utcnow().isoformat()}] Sent to {record_metadata.topic} "
                          f"partition={record_metadata.partition} offset={record_metadata.offset}")
                except Exception as err:
                    print(f"Failed to send message: {err}")

                producer.flush()

            time.sleep(KAFKA_FETCH_INTERVAL)

    except KeyboardInterrupt:
        print("Interrupted by user, closing producer...")
    finally:
        producer.close()


if __name__ == "__main__":
    main()
            
