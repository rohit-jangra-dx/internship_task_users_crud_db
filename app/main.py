from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.config import config
from app.routes import router as users_router
import app.db as db

@asynccontextmanager
async def lifespan(app: FastAPI):
    db.sessionmanager = db.DatabaseSessionManager(
        config.database_url,
        {"echo": config.echo_sql}
    )
    yield 
    await db.sessionmanager.close()

app = FastAPI(lifespan=lifespan)
app.include_router(users_router)



