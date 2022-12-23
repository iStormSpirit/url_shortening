from typing import Generic, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import logger
from db.db import Base

from .security import get_password_hash

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)


class Repository:
    def get(self, *args, **kwargs):
        raise NotImplementedError

    def create(self, *args, **kwargs):
        raise NotImplementedError

    def update(self, *args, **kwargs):
        raise NotImplementedError

    def delete(self, *args, **kwargs):
        raise NotImplementedError


class RepositoryDB(Repository, Generic[ModelType, CreateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self._model = model

    async def get(self, db: AsyncSession, user_id: int) -> ModelType | None:
        statement = select(self._model).where(self._model.id == user_id)
        results = await db.execute(statement=statement)
        logger.info(f'get user by id {user_id}')
        return results.scalar_one_or_none()

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        hash_password = get_password_hash(obj_in.dict().pop('password'))
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data['password'] = hash_password
        logger.info(f'hashed password for {obj_in_data}')
        db_obj = self._model(**obj_in_data)
        logger.info(f'user created {obj_in_data}')
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: AsyncSession, *, db_obj: ModelType, obj_in) -> ModelType:
        pass

    async def delete(self, db: AsyncSession, *, user_id: int) -> ModelType | None:
        db_obj = await self.get(db=db, user_id=user_id)
        if not db_obj:
            logger.info(f'not found user with id {user_id}')
            return None
        logger.info(f'deleted user by id {user_id}')
        await db.delete(db_obj)
        await db.commit()
        return db_obj

    async def get_username(self, db: AsyncSession, username: str) -> ModelType | None:
        statement = select(self._model).where(self._model.username == username)
        results = await db.execute(statement=statement)
        logger.info(f'get user by username {username}')
        return results.scalar_one_or_none()
