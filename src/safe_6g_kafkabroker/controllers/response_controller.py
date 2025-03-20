from fastapi import APIRouter
from safe_6g_kafkabroker.models.function_response import FunctionResponse
from safe_6g_kafkabroker.services.kafka_producer_service import kafka_producer
from safe_6g_kafkabroker.models.kafka_message import FunctionType

router = APIRouter()

@router.post("/function/publish/{function}")
async def send_response(function: FunctionType, response: FunctionResponse):
    """Function components send response messages to the Cognitive Coordinator."""
    topic = f"trust.{function.lower()}.response"
    await kafka_producer.send_message(topic, response.model_dump())
    return {"status": "Response sent", "topic": topic}
