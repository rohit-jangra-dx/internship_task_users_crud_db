from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.models import UserDB
from app.schemas import UserCreate, UserRead

router = APIRouter(prefix="/users", tags=["users"])

DBSession = Annotated[AsyncSession, Depends(get_db)]


@router.get("", response_model=list[UserRead], status_code=status.HTTP_200_OK)
async def list_users(db: DBSession): 
    result = await db.execute(select(UserDB))
    return result.scalars().all()
    

@router.get("/{user_id}", response_model=UserRead, status_code=status.HTTP_200_OK)
async def get_user(user_id: UUID, db: DBSession):
    result = await db.execute(
        select(UserDB).where(UserDB.id == user_id)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user 

@router.post("", response_model=UserRead,  status_code=status.HTTP_201_CREATED)
async def create_user(payload: UserCreate, db: DBSession):
    user = UserDB(**payload.model_dump())
    db.add(user)
    
    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )
    
    await db.refresh(user)
    return user

@router.put("/{user_id}", response_model=UserRead, status_code=status.HTTP_200_OK)
async def update_user(
    user_id: UUID, 
    payload: UserCreate, 
    db: DBSession,
):
    result = await db.execute(
        select(UserDB).where(UserDB.id == user_id)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
        
    for field, value in payload.model_dump().items():
        setattr(user, field, value)
    
    await db.commit()
    await db.refresh(user)
    return user
    
    
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: UUID, db: DBSession):
    result = await db.execute(
        select(UserDB).where(UserDB.id == user_id)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
        
    await db.delete(user)
    await db.commit()
    