import os
import logging
from kafka import KafkaProducer
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

producer = None


def get_kafka_producer():
    global producer

    if producer is not None:
        return producer

    bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS")

    if not bootstrap_servers:
        logger.warning("Kafka is disabled: KAFKA_BOOTSTRAP_SERVERS not found.")
        return None

    try:
        producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            security_protocol="SASL_SSL",
            sasl_mechanism="SCRAM-SHA-256",
            sasl_plain_username=os.getenv("KAFKA_USERNAME"),
            sasl_plain_password=os.getenv("KAFKA_PASSWORD"),
            ssl_cafile=os.getenv("KAFKA_CA_CERT"),
            value_serializer=lambda v: v.encode("utf-8"),
            request_timeout_ms=10000,
            api_version_auto_timeout_ms=10000,
        )

        logger.info("Kafka connected successfully.")
        return producer

    except Exception as e:
        logger.warning("Kafka unavailable: %s", e)
        producer = None
        return None


def send_kafka_event(message):
    kafka_producer = get_kafka_producer()

    if kafka_producer is None:
        return False

    try:
        topic = os.getenv("KAFKA_TOPIC")

        if not topic:
            logger.warning("KAFKA_TOPIC is not configured.")
            return False

        kafka_producer.send(topic, message)
        kafka_producer.flush(timeout=5)

        return True

    except Exception as e:
        logger.warning("Kafka event could not be sent: %s", e)
        return False