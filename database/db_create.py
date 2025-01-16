from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from typing import AsyncGenerator


DATABASE_URL = str("postgresql+asyncpg://postgres:0101@localhost/application")

engine = create_async_engine(url=DATABASE_URL, echo=True)
async_session = sessionmaker(bind=engine, class_= AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as db:
        yield db