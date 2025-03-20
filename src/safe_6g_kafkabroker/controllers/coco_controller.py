from fastapi import APIRouter
from safe_6g_kafkabroker.models.kafka_message import FunctionType
from safe_6g_kafkabroker.services.kafka_consume_service import kafka_consumer

router = APIRouter()

@router.get("/cognitive/consume/{function}")
async def consume_function_responses(function: FunctionType, limit: int = 5, timeout: int = 5):
    """
    Cognitive Coordinator retrieves responses from function components.
    """
    topic = f"trust.{function.lower()}.response"
    messages = await kafka_consumer.start_consumer(topic, max_messages=limit, timeout=timeout)
    return {"function": function, "responses": messages}
