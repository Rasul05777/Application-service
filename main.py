from fastapi import FastAPI

from routers.router import router as router_application

from app.config import settings

from kafka.kafka_producer import KafkaProducer


producer = KafkaProducer(settings.kafka_brokers, settings.kafka_topic)


def lifespan(app: FastAPI):
    async def start():
        print("Запуск kafka producer")
        await producer.start()
        
        
    async def stop():
        print("Завершение kafka producer")
        await producer.stop()
        
    return start, stop
    

app = FastAPI(lifespan=lifespan)



app.include_router(router_application)