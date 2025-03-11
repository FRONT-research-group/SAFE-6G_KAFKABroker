from fastapi import APIRouter

from safe_6g_kafkabroker.utils.logging import setup_logger
from safe_6g_kafkabroker.models.kafka_message import KafkaMessage, FunctionType

router = APIRouter()
logger = setup_logger(logger_name="KafkaController")

@router.post("/publish")
async def publish(message: KafkaMessage):
    return {"message": message}


@router.get("/subscribe/{function}")
async def consume(function: FunctionType, limit: int = 10):
    return {"messages": [f"Message {i}" for i in range(limit)]}