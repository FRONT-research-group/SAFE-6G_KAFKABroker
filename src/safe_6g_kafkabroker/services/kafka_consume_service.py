import os
import json

from kafka import KafkaConsumer

from safe_6g_kafkabroker.models.kafka_message import FunctionType

KAFKA_SERVER = os.getenv("KAFKA_SERVER", "localhost:9092")

class KafkaConsumerService:
    def __init__(self, function_type: FunctionType):
        self.topic = function_type.value
        self.consumer = KafkaConsumer(
            self.topic,
            bootstrap_servers=KAFKA_SERVER,
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
            auto_offset_reset="earliest",
            enable_auto_commit=True,
        )

    def consume_messages(self, limit: int = 10):
        messages = []
        for message in self.consumer:
            messages.append(message.value)
            if len(messages) >= limit:
                break
        return messages
