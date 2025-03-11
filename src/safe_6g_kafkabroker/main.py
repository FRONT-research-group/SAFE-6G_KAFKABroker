from fastapi import FastAPI

from safe_6g_kafkabroker.api.api import api_router
from safe_6g_kafkabroker.utils.logging import setup_logger

loggin = setup_logger(logger_name="BrokerAPI")

app = FastAPI(title="Kafka FastAPI Microservice", version="1.0.0")
app.include_router(api_router, prefix="/kafka")


