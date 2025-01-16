from aiokafka import AIOKafkaProducer
import json


class KafkaProducer:
    def __init__(self, brokers: str, topic: str):
        self.producer = AIOKafkaProducer(bootstrap_servers=brokers)
        self.topic = topic
        
        
    async def start(self):
        await self.producer.start()
        
        
    async def stop(self):
        await self.producer.stop()
        
    
    async def send(self, message: dict):
        value = json.dumps(message).encode('utf-8')
        await self.producer.send_and_wait(self.topic, value)
        