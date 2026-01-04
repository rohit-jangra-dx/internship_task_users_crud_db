from typing import  AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession
import app.db as db 

async def get_db() -> AsyncIterator[AsyncSession]:
    assert db.sessionmanager is not None, "Db not initialized"
    async with db.sessionmanager.session() as session:
        yield session
    