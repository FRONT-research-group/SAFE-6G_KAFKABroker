from fastapi import APIRouter

from safe_6g_kafkabroker.models.kafka_message import KafkaMessage
from safe_6g_kafkabroker.services.kafka_producer_service import kafka_producer
from safe_6g_kafkabroker.models.kafka_message import FunctionType

router = APIRouter()

@router.post("/cognitive/publish/{function}")
async def publish_message(function: FunctionType, msg: KafkaMessage):
    """Cognitive Coordinator publishes messages to function topics."""
    topic = f"trust.{function.lower()}"
    await kafka_producer.send_message(topic, msg.model_dump())
    return {"status": "Message published", "topic": topic}
