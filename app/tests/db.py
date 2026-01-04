from app.db import DatabaseSessionManager
from app.config import config

assert "test" in config.test_database_url.lower(), \
    "Don't create test db session on non-test database"
    
test_sessionmanager = DatabaseSessionManager(config.test_database_url,{"echo": True})