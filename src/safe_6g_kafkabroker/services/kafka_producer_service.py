import os
import json

from kafka import KafkaProducer
from safe_6g_kafkabroker.models.kafka_message import KafkaMessage

KAFKA_SERVER = os.getenv("KAFKA_SERVER", "kafka:9092")

class KafkaProducerService:
    """
    KafkaProducerService is responsible for publishing messages to Kafka topics.
    
    This service serializes messages into JSON format and sends them to a Kafka topic 
    determined by the message's function type. It ensures that messages are flushed to the broker,
    supporting a reliable, asynchronous messaging system that other components (or teams) can use 
    to communicate within the SAFE-6G framework.
    
    Attributes:
        producer (KafkaProducer): The underlying Kafka producer instance configured with the
                                  target Kafka server and a JSON serializer.
    """
    def __init__(self):
        """
        Initialize the KafkaProducerService.

        Notes:
            - Ensure that the topics are configured with adequate partitioning on your Kafka cluster.
            - The producer uses a JSON serializer for outgoing messages.
        """
        self.producer = KafkaProducer(
            bootstrap_servers=KAFKA_SERVER,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )

    def send_message(self, message: KafkaMessage):
        """
        Publish a message to a Kafka topic.

        Args:
            message (KafkaMessage): The message to publish.

        Returns:
            Status (dict): A dictionary with a status message regarding the publishing result.
        """
        topic = message.function.value  # Use function type as topic
        self.producer.send(topic, message.model_dump())
        self.producer.flush()
        return {"status": "Message published to topic: " + topic}
