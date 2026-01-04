from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.dependencies import get_users_store
from app.models import User
from app.db import UsersInMemoryStore

router = APIRouter(prefix="/users")


@router.get("", response_model=list[User], status_code=status.HTTP_200_OK)
def list_users(
    store: UsersInMemoryStore = Depends(get_users_store),
): 
    return store.list()

@router.get("/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
def get_user(
    user_id: UUID,
    store: UsersInMemoryStore = Depends(get_users_store),
):
    return store.get(user_id)

@router.post("", response_model=User,  status_code=status.HTTP_201_CREATED)
def create_user(
    user: User,
    store: UsersInMemoryStore = Depends(get_users_store),
):
    store.create(user)
    return user

@router.put("/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
def update_user(
    user_id: UUID, 
    user: User, 
    store: UsersInMemoryStore = Depends(get_users_store),
):
    if user.id != user_id:
        raise HTTPException(status_code=400, detail="ID mismatch")
        
    store.update(user_id, user)
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: UUID,
    store: UsersInMemoryStore = Depends(get_users_store),
):
    store.delete(user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    