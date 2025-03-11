import os
import json

from kafka import KafkaProducer

from safe_6g_kafkabroker.models.kafka_message import KafkaMessage

KAFKA_SERVER = os.getenv("KAFKA_SERVER", "localhost:9092")

class KafkaProducerService:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=KAFKA_SERVER,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )

    def send_message(self, message: KafkaMessage):
        topic = message.function.value  # Use function type as topic
        self.producer.send(topic, message.model_dump())
        self.producer.flush()
        return {"status": "Message published to topic: " + topic}
