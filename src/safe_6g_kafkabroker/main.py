from fastapi import FastAPI
from contextlib import asynccontextmanager

from safe_6g_kafkabroker.controllers import publish_controller, consume_controller, response_controller, coco_controller
from safe_6g_kafkabroker.services.kafka_producer_service import kafka_producer

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler to manage Kafka startup and shutdown."""
    print("Starting Kafka Producer...")
    await kafka_producer.start()
    yield  # Hand control over to the application
    print("Shutting down Kafka Producer...")
    await kafka_producer.stop()

app = FastAPI(title="Kafka Message Broker for SAFE-6G")

# Include Routes
app.include_router(publish_controller.router, prefix="/api")
app.include_router(coco_controller.router, prefix="/api")
app.include_router(response_controller.router, prefix="/api")
app.include_router(consume_controller.router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)