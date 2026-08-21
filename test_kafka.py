from kafka_config import send_kafka_event

print("Connecting to Kafka...")

try:
    send_kafka_event("Hello from Bhawna Portfolio!")
    print("Kafka event sent successfully!")
except Exception as e:
    print("Kafka connection failed!")
    print("Error:", e)