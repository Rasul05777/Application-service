import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from service.queries import create_application, get_all, get_application, delete_application
from models.model_application import Application
from schemas.schemas_application import ApplicationCreate

DATABASE_URL = "postgresql+asyncpg://postgres:0101@localhost/test_application"

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

@pytest.fixture
async def db_session():
    async with engine.begin() as conn:
        await conn.run_sync(Application.metadata.create_all)
    async with AsyncSessionLocal() as session:
        yield session
    async with engine.begin() as conn:
        await conn.run_sync(Application.metadata.drop_all)

@pytest.mark.asyncio
async def test_create_application(db_session: AsyncSession):
    application_data = ApplicationCreate(user_name="test_user", description="test_description")
    application = await create_application(db_session, application_data)
    assert application.user_name == "test_user"
    assert application.description == "test_description"

@pytest.mark.asyncio
async def test_get_all(db_session: AsyncSession):
    applications = await get_all(db_session)
    assert len(applications) == 0

@pytest.mark.asyncio
async def test_get_application(db_session: AsyncSession):
    application_data = ApplicationCreate(user_name="test_user", description="test_description")
    await create_application(db_session, application_data)
    applications = await get_application(db_session, "test_user")
    assert len(applications) == 1

@pytest.mark.asyncio
async def test_delete_application(db_session: AsyncSession):
    application_data = ApplicationCreate(user_name="test_user", description="test_description")
    await create_application(db_session, application_data)
    message = await delete_application(db_session, "test_user")
    assert message == "Application with user_name test_user successfuly deleted"