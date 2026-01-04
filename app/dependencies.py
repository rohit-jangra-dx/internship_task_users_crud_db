from typing import  AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession
from app.db import sessionmanager

async def get_db() -> AsyncIterator[AsyncSession]:
    async with sessionmanager.session() as session:
        yield session
    