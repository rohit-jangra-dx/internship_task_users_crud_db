import pytest
from uuid import UUID


@pytest.mark.anyio
async def test_create_user_success(client):
    payload = {
        "name": "Alice",
        "email": "alice@test.com",
        "age": 25,
    }

    res = await client.post("/users", json=payload)

    assert res.status_code == 201
    data = res.json()

    assert UUID(data["id"])
    assert data["name"] == payload["name"]
    assert data["email"] == payload["email"]
    assert data["age"] == payload["age"]

@pytest.mark.anyio
async def test_create_user_duplicate_email(client):
    payload = {
        "name": "Alice",
        "email": "alice@test.com",
        "age": 25,
    }

    await client.post("/users", json=payload)
    res = await client.post("/users", json=payload)

    assert res.status_code == 409


@pytest.mark.anyio 
async def test_get_user_success(client):
    create = await client.post(
        "/users",
        json={
            "name": "charlie",
            "email": "charlie@gmail.com",
            "age": 28, 
        }
    )
    
    user_id = create.json()["id"]
    
    res = await client.get(f"/users/{user_id}")
    
    assert res.status_code == 200
    assert res.json()["id"] == user_id

@pytest.mark.anyio
async def test_get_user_not_found(client):
    res = await client.get(
        "/users/00000000-0000-0000-0000-000000000000"
    )

    assert res.status_code == 404


@pytest.mark.anyio
async def test_list_users_empty(client):
    res = await client.get("/users")

    assert res.status_code == 200
    assert res.json() == []

@pytest.mark.anyio
async def test_list_users_with_data(client):
    await client.post(
        "/users",
        json={"name": "Aron", "email": "a@test.com", "age": 20},
    )
    await client.post(
        "/users",
        json={"name": "Baron", "email": "b@test.com", "age": 21},
    )

    res = await client.get("/users")

    assert res.status_code == 200
    data = res.json()
    print("\nLIST USERS RESPONSE:")
    print(data)
    assert len(data) == 2
    emails = {u["email"] for u in data}
    assert emails == {"a@test.com", "b@test.com"}

@pytest.mark.anyio
async def test_update_user_success(client):
    create = await client.post(
        "/users",
        json={"name": "Old", "email": "old@test.com", "age": 40},
    )

    user_id = create.json()["id"]

    res = await client.put(
        f"/users/{user_id}",
        json={"name": "New", "email": "new@test.com", "age": 45},
    )

    assert res.status_code == 200
    assert res.json()["name"] == "New"

@pytest.mark.anyio
async def test_delete_user_success(client):
    create = await client.post(
        "/users",
        json={"name": "Del", "email": "del@test.com", "age": 35},
    )

    user_id = create.json()["id"]

    res = await client.delete(f"/users/{user_id}")
    assert res.status_code == 204

    res = await client.get(f"/users/{user_id}")
    assert res.status_code == 404
