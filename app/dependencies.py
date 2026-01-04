from app.db import UsersInMemoryStore

# This single instance will be shared
_users_store = UsersInMemoryStore()

# via this function
def get_users_store() -> UsersInMemoryStore:
    return _users_store