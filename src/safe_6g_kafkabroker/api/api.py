from fastapi import APIRouter

from safe_6g_kafkabroker.controllers.kafka_controller import router as kafka_router

api_router = APIRouter()
api_router.include_router(kafka_router, tags=["Kafka"])
