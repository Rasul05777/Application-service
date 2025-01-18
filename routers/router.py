from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from models.model_application import Application
from database.db_create import get_db
from service.queries import create_application, get_application, get_all, delete_application
from schemas.schemas_application import ApplicationCreate, ApplicationResponse
from typing import List
from kafka.kafka_producer import KafkaProducer
from app.config import settings

router = APIRouter(
    prefix="/application",
    tags=["Заявки"]
)

async def get_kafka_producer():
    producer = KafkaProducer(settings.kafka_brokers, settings.kafka_topic)
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()

@router.post("", response_model=ApplicationCreate, summary="Создание заявки")
async def post_application(
    application: ApplicationCreate, 
    db: AsyncSession = Depends(get_db),
    producer: KafkaProducer = Depends(get_kafka_producer)
):
    app = await create_application(db, application)
    await producer.send({
        "id": app.id,
        "user_name": app.user_name,
        "description": app.description,
        "created_at": str(app.created_at)
    })
    return app   

@router.get("", response_model=List[ApplicationResponse], summary="Список всех заявок")
async def get_all_applications(
    page: int = 1, 
    size: int = 10, 
    db: AsyncSession = Depends(get_db)
):
    return await get_all(db, page, size)

@router.get("/{name}", response_model=List[ApplicationResponse], summary="Поиск заявки по имени")
async def get_application_by_name(
    user_name: str, 
    page: int = 1, 
    size: int = 10,  
    db: AsyncSession = Depends(get_db)
):
    return await get_application(db, user_name, page, size)

@router.delete("/{name}", summary="Удаление заявки по имени")
async def delete_application_by_name(
    user_name: str, 
    db: AsyncSession = Depends(get_db)
):
    return await delete_application(db, user_name)