import pytest
from kafka.kafka_producer import KafkaProducer
from app.config import settings

@pytest.mark.asyncio
async def test_kafka_producer():
    producer = KafkaProducer(settings.kafka_brokers, settings.kafka_topic)
    await producer.start()
    await producer.send({"key": "value"})
    await producer.stop()