from abc import ABC, abstractmethod
from typing import Generic, Optional, Type, TypeVar

import pyshorteners
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import logger
from db.db import Base

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

    async def get(self, db: AsyncSession, url_id: int) -> ModelType | None:
        logger.info(f'get function get: {url_id}')
        statement = select(self._model).where(self._model.id == url_id)
        obj = await db.scalar(statement=statement)
        return obj

    async def update(self, *args, **kwargs):
        pass

    @staticmethod
    def shortener(url: str) -> str:
        logger.info(f'shortener function get: {url}')
        shortener = pyshorteners.Shortener()
        short_url = shortener.tinyurl.short(url)
        logger.info(f'shortener function return: {short_url}')
        return short_url

    async def create(self, db: AsyncSession, obj_url: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_url)
        logger.info(f'create function created: {obj_in_data}')
        obj_in_data['short_url'] = self.shortener(obj_in_data['original_url'])
        db_obj = self._model(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, url_id: int) -> ModelType | None:
        db_obj = await self.get(db=db, url_id=url_id)
        if not db_obj:
            return None
        logger.info(f'delete function deleted: {db_obj} with id {url_id}')
        await db.delete(db_obj)
        await db.commit()
        return db_obj

    # async def get_status(self, db: AsyncSession, url_id: int) -> ModelType | None:
    #     url = await self.get_item(db, url_id)
    #     if not url.private:
    #         return url.usage_count
