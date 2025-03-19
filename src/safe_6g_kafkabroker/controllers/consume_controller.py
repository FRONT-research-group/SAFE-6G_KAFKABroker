from fastapi import APIRouter

from safe_6g_kafkabroker.models.kafka_message import FunctionType
from safe_6g_kafkabroker.services.kafka_consume_service import kafka_consumer

router = APIRouter()

@router.get("/function/consume/{function}")
async def consume_messages(function: FunctionType, limit: int = 5):
    """Function Owners retrieve latest messages for their function."""
    topic = f"trust.{function.lower()}"
    messages = await kafka_consumer.start_consumer(topic, max_messages=limit)
    return {"function": function, "messages": messages}
