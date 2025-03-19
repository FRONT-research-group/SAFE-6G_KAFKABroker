import os
import json

from aiokafka import AIOKafkaProducer

from safe_6g_kafkabroker.utils.logging import setup_logger

logger = setup_logger()

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")

class KafkaProducerService:
    def __init__(self):
        self.producer = None

    async def start(self):
        """Start the Kafka producer."""
        self.producer = AIOKafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        await self.producer.start()
        logger.info("Kafka Producer started.")

    async def send_message(self, topic: str, message: dict):
        """Send message to Kafka topic."""
        if not self.producer:
            await self.start()
        await self.producer.send(topic, message)
        logger.info(f"Message sent to topic `{topic}`: {message}")

    async def stop(self):
        """Stop Kafka producer."""
        if self.producer:
            await self.producer.stop()
            logger.info("Kafka Producer stopped.")

# Initialize a global instance
kafka_producer = KafkaProducerService()
