import os
import json

from kafka import KafkaConsumer
from safe_6g_kafkabroker.models.kafka_message import FunctionType

KAFKA_SERVER = os.getenv("KAFKA_SERVER", "kafka:9092")

class KafkaConsumerService:
    """
    KafkaConsumerService handles consuming messages from a specific Kafka topic based on function type.
    
    This service subscribes to a Kafka topic corresponding to the provided function type (e.g., SAFETY, SECURITY).
    It deserializes JSON messages and retrieves a batch of messages up to a specified limit. The consumer is configured 
    to manage offsets manually, ensuring precise control over message processing within a pull-based API model.
    
    Attributes:
        topic (str): The Kafka topic to subscribe to, derived from the function type.
        consumer (KafkaConsumer): The underlying Kafka consumer instance.
    """
    def __init__(self, function_type: FunctionType):
        """
        Initialize a Kafka consumer to subscribe to a given function topic.

        Args:
            function_type (FunctionType): The type of function to subscribe to.

        Notes:
            - Topics should be pre-configured on your Kafka cluster with appropriate partitioning.
            - auto_offset_reset is set to 'earliest' to start from the beginning if no offset is committed.
            - enable_auto_commit is disabled to allow for manual offset management.
        """
        self.topic = function_type.value  # Subscribe to function topic
        group_id = f"{function_type.value.lower()}-consumer-group"
        self.consumer = KafkaConsumer(
            self.topic,
            bootstrap_servers=KAFKA_SERVER,
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
            auto_offset_reset="earliest",
            enable_auto_commit=False,  # Disable auto commit for manual offset control
            group_id=group_id,
            consumer_timeout_ms=5000  
        )

    def consume_messages(self, limit: int = 10):
        """
        Consume messages from the Kafka topic and manually commit offsets after processing.

        Args:
            limit (int): The maximum number of messages to consume.

        Returns:
            messages(list): A list of consumed messages.

        Notes:
            - Offsets are manually committed after processing the batch to ensure reliability.
            - The consumer is closed gracefully once processing is complete.
        """
        messages = []
        try:
            for message in self.consumer:
                messages.append(message.value)
                if len(messages) >= limit:
                    break
            # Manually commit offsets after processing the batch
            self.consumer.commit()
        finally:
            self.consumer.close()
        return messages
