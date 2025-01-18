from fastapi import FastAPI, Depends
from routers.router import router as router_application
from app.config import settings
from kafka.kafka_producer import KafkaProducer

async def get_kafka_producer():
    producer = KafkaProducer(settings.kafka_brokers, settings.kafka_topic)
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()

def lifespan(app: FastAPI):
    async def start():
        print("Запуск kafka producer")
        # KafkaProducer будет создан и запущен через Depends в роутере
        
    async def stop():
        print("Завершение kafka producer")
        # KafkaProducer будет остановлен через Depends в роутере
        
    return start, stop

app = FastAPI(lifespan=lifespan)
app.include_router(router_application)