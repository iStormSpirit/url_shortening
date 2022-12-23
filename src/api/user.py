from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import logger
from db.db import get_session
from schemas import user as user_schema
from services.base import user_crud

router = APIRouter()


@router.get('/user/{id}', response_model=user_schema.User, tags=['user crud'])
async def get_user_by_id(*, db: AsyncSession = Depends(get_session), user_id: int) -> Any:
    user = await user_crud.get(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='users by id not found')
    return user


@router.post('/register', response_model=user_schema.User, status_code=status.HTTP_201_CREATED, tags=['user crud'])
async def create_user(*, db: AsyncSession = Depends(get_session), data: user_schema.UserCreate) -> Any:
    user = await user_crud.create(db=db, obj_in=data)
    logger.info(f'user: {data.username} is created')
    return user


@router.delete('/user/{id}/delete', tags=['user crud'])
async def delete_user(*, db: AsyncSession = Depends(get_session), user_id: int) -> Any:
    user = await user_crud.delete(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found')
    return user
