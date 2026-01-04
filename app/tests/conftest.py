import pytest 
from sqlalchemy import text
from httpx import AsyncClient, ASGITransport

from app.main import app 
from app.dependencies import get_db
from app.db import DatabaseSessionManager
from app.config import config

@pytest.fixture
async def test_sessionmanager():
    assert "test" in config.test_database_url.lower(), \
        "Don't create test db session on non-test database"
    
    manager = DatabaseSessionManager(config.test_database_url,{"echo": True})
    yield manager 
    await manager.close()


TABLES = ["users"]   

@pytest.fixture(autouse=True)
async def reset_database(test_sessionmanager):
    async with test_sessionmanager.session() as session:
        for table in TABLES:
            await session.execute(
                text(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE")
            )

        await session.commit()
    
    
@pytest.fixture
async def client(test_sessionmanager):
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