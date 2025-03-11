from fastapi import APIRouter

from safe_6g_kafkabroker.utils.logging import setup_logger
from safe_6g_kafkabroker.models.kafka_message import KafkaMessage, FunctionType
from safe_6g_kafkabroker.services import KafkaProducerService, KafkaConsumerService

router = APIRouter()
logger = setup_logger(logger_name="KafkaController")

@router.post("/publish")
async def publish(message: KafkaMessage):
    return KafkaProducerService().send_message(message)

@router.get("/consume/{function}")
async def consume(function: FunctionType, limit: int = 10):
    consumer_service = KafkaConsumerService(function)
    return {"messages": consumer_service.consume_messages(limit)}