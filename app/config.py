from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    kafka_brokers: str
    kafka_topic: str
    
    class Config:
        env_file = ".env"
        

settings = Settings()