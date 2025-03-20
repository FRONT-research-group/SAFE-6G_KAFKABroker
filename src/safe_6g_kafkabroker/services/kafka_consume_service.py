import os
import json
import asyncio

from aiokafka import AIOKafkaConsumer

from safe_6g_kafkabroker.utils.logging import setup_logger

logger = setup_logger()

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")

class KafkaConsumerService:
    def __init__(self):
        self.consumer = None

    async def start_consumer(self, topic: str, max_messages: int = 10, timeout: int = 5):
        """Consume the latest messages from a Kafka topic with timeout handling."""
        self.consumer = AIOKafkaConsumer(
            topic,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            auto_offset_reset="earliest",  # 'earliest' ensures it gets old messages if available
            enable_auto_commit=True,
            group_id="fastapi-consumer-group"  # Consumers with the same group share messages
        )

        await self.consumer.start()
        logger.info(f"Subscribed to `{topic}`, waiting for messages...")

        messages = []
        try:
            while len(messages) < max_messages:
                msg = await asyncio.wait_for(self.consumer.getone(), timeout)  # ⏳ Timeout Handling
                messages.append(json.loads(msg.value))
                logger.info(f"Received message from `{topic}`: {messages[-1]}")
        except asyncio.TimeoutError:
            logger.warning(f"No new messages in `{topic}` within {timeout} seconds. Returning what we have.")

        await self.consumer.stop()
        return messages

# Global instance
kafka_consumer = KafkaConsumerService()
