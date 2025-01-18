import pytest
from fastapi.testclient import TestClient
from main import app
from sqlalchemy.ext.asyncio import  AsyncSession

client = TestClient(app)

@pytest.mark.asyncio
async def test_create_application(db_session: AsyncSession):
    response = client.post("/application", json={"user_name": "test_user", "description": "test_description"})
    assert response.status_code == 200
    assert response.json()["user_name"] == "test_user"

@pytest.mark.asyncio
async def test_get_all(db_session: AsyncSession):
    response = client.get("/application")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_application_by_name(db_session: AsyncSession):
    response = client.get("/application/test_user")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_delete_application_by_name(db_session: AsyncSession):
    response = client.delete("/application/test_user")
    assert response.status_code == 200