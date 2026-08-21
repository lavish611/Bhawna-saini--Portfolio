import os
from kafka import KafkaProducer
from dotenv import load_dotenv

load_dotenv()

producer = KafkaProducer(
    bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
    security_protocol="SASL_SSL",
    sasl_mechanism="SCRAM-SHA-256",
    sasl_plain_username=os.getenv("KAFKA_USERNAME"),
    sasl_plain_password=os.getenv("KAFKA_PASSWORD"),
    ssl_cafile=os.getenv("KAFKA_CA_CERT"),
    value_serializer=lambda v: v.encode("utf-8")
)

def send_kafka_event(message):
    producer.send(
        os.getenv("KAFKA_TOPIC"),
        message
    )
    producer.flush()