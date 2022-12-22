# from typing import Any
# from logging import config, getLogger
# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.ext.asyncio import AsyncSession
#
# from core.logger import LOGGING
# from db.db import get_session
# from schemas import user as user_schema
# from services.base import user_crud
#
# router = APIRouter()
#
# config.dictConfig(LOGGING)
# logger = getLogger(__name__)
#
#
# @router.post('/register', response_model=user_schema.User, status_code=status.HTTP_201_CREATED,
#              tags=['endpoints', 'user crud'])
# async def create_user(*, db: AsyncSession = Depends(get_session), data: user_schema.UserCreate) -> Any:
#     """
#     :param db: currently db
#     :param data: username and password for creating user
#     :return: created user
#     """
#     user = await user_crud.create(db=db, obj_in=data)
#     logger.info(f'user: {data.username} is created')
#     return user
