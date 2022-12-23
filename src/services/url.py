import time
from typing import Generic, Type, TypeVar

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

    async def update_usage_count(self, db: AsyncSession, url_id: int, counter: int):
        logger.info(f'update usage_count for id: {url_id}')
        stm = update(self._model).where(self._model.id == url_id).values(usage_count=counter + 1)
        await db.execute(stm)
        await db.commit()

    async def get(self, db: AsyncSession, url_id: int) -> ModelType | None:
        logger.info(f'get function get: {url_id}')
        statement = select(self._model).where(self._model.id == url_id)
        obj = await db.scalar(statement=statement)
        if not obj:
            return None
        if obj.is_archived is True:
            return 410
        return obj

    async def get_redirect(self, db: AsyncSession, url_id: int) -> ModelType | None:
        logger.info(f'get function get: {url_id}')
        statement = select(self._model).where(self._model.id == url_id)
        obj = await db.scalar(statement=statement)
        if not obj:
            return None
        if obj.is_archived is True:
            return 410
        counter = obj.usage_count
        await self.update_usage_count(db=db, url_id=url_id, counter=counter)
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

    async def create_list(self, db: AsyncSession, obj_url: str):
        obj_in_data = dict()
        logger.info(f'create22 function get: {obj_in_data}')
        obj_in_data['original_url'] = obj_url
        obj_in_data['short_url'] = self.shortener(obj_url)
        db_obj = self._model(**obj_in_data)
        db.add(db_obj)
        logger.info(f'create22 function created: {db_obj}')
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

    async def get_ping_db(self, db: AsyncSession) -> dict | None:
        start_time = time.time()
        statement = select(self._model)
        await db.execute(statement=statement)
        ping = time.time() - start_time
        return {
            'db': '{:.4f}'.format(ping),
        }

    async def archived(self, db: AsyncSession, url_id: int) -> ModelType | None:
        db_obj = await self.get(db=db, url_id=url_id)
        stm = update(self._model).where(self._model.id == url_id).values(is_archived=True)
        logger.info(f'archived function archived: {db_obj} with id {url_id}')
        await db.execute(stm)
        await db.commit()
        if not db_obj:
            return None
