from uuid import UUID

import pytest

@pytest.mark.asyncio
async def test_create_user(client):
    payload = {
        "name": "Anything",
        "email": "Anything@test.com",
        "age": 20
    }
    
    res = await client.post("/users", json=payload)
    
    assert res.status_code == 201 
    data = res.json() 
    
    assert UUID(data["id"])
    assert data["email"] == payload["email"]
    