import asyncio
import pytest 
import pytest_asyncio
from typing import AsyncIterator

from httpx import AsyncClient, ASGITransport
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app 
from app.tests.db import test_sessionmanager
from app.dependencies import get_db

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

TABLES = ["users"]   

@pytest_asyncio.fixture(autouse=True)
async def reset_database():
    async with test_sessionmanager.session() as session:
        for table in TABLES:
            await session.execute(
                text(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE")
            )

        await session.commit()
    
    
@pytest_asyncio.fixture
async def client():
    async def override_get_db():
        async with test_sessionmanager.session() as session:
            yield session
    
    app.dependency_overrides[get_db] = override_get_db
    
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, 
        base_url="http://test"
    ) as c:
        yield c 
    
    app.dependency_overrides.clear()