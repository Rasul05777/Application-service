from fastapi import HTTPException

from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.model_application import Application

from schemas.schemas_application import ApplicationCreate, ApplicationResponse


async def create_application(db: AsyncSession, application_data: ApplicationCreate) -> Application:
    application = Application(
        user_name = application_data.user_name,
        description = application_data.description
        )
    
    db.add(application)
    await db.commit()
    await db.refresh(application)
    return application


async def get_all(db: AsyncSession, page: int = 1, size: int = 10) -> List[Application]:
    query = select(Application)
    query = await db.execute(query.offset((page -1) * size).limit(size))
    if not query:
        raise HTTPException(status_code=404, detail="Applications not found")
    return query.scalars().all()
    

async def get_application(db: AsyncSession, user_name: str, page: int = 1, size: int = 10) -> List[Application]:
    query = select(Application)
    if user_name:
        query = query.filter(Application.user_name == user_name) 
    else:
        raise HTTPException(status_code=404, detail="Applications not found")
    result = await db.execute(query.offset((page -1) * size).limit(size))
    return result.scalars().all()


async def delete_application(db: AsyncSession, user_name: str) -> str:
    query = await db.execute(select(Application).where(Application.user_name==user_name))
    result = query.scalar_one_or_none
    if not result:
        raise HTTPException(status_code=404, detail="Applications not found")
    
    await db.delete(result)
    await db.commit()
    
    return f"Application with user_name {user_name} successfuly deleted"
