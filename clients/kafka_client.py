from confluent_kafka import Consumer
from kafka import KafkaProducer
from config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_BOOTSTRAP_SERVERS_LOCAL, KAFKA_GROUP_ID
import json


def create_kafka_consumer():
    return Consumer({
            'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS_LOCAL,
            'group.id': KAFKA_GROUP_ID,
            'auto.offset.reset': 'earliest',
            'enable.auto.commit': False
        })

def create_kafka_producer():
    return KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)