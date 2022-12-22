# import time
# from typing import Any, Generic, Type, TypeVar
#
# from fastapi.encoders import jsonable_encoder
# from pydantic import BaseModel
# from sqlalchemy import select
# from sqlalchemy.ext.asyncio import AsyncSession
#
# from db.db import Base
#
# ModelType = TypeVar('ModelType', bound=Base)
# CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
# UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)
#
#
# class Repository:
#
#     def get(self, *args, **kwargs):
#         raise NotImplementedError
#
#     def create(self, *args, **kwargs):
#         raise NotImplementedError
#
#     def update(self, *args, **kwargs):
#         raise NotImplementedError
#
#     def delete(self, *args, **kwargs):
#         raise NotImplementedError
#
#
# class RepositoryDB(Repository, Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
#
#     def __init__(self, model: Type[ModelType]):
#         self._model = model
#
#     async def get(self, db: AsyncSession, id: int) -> ModelType | None:
#         statement = select(self._model).where(self._model.id == id)
#         results = await db.execute(statement=statement)
#         return results.scalar_one_or_none()
#
#     async def get_multi(self, db: AsyncSession, *, skip=0, limit=100) -> list[ModelType]:
#         statement = select(self._model).offset(skip).limit(limit)
#         results = await db.execute(statement=statement)
#         return results.scalars().all()
#
#     async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
#         # hash_password = get_password_hash(obj_in.dict().pop('password'))
#         obj_in_data = jsonable_encoder(obj_in)
#         # obj_in_data['password'] = hash_password
#         db_obj = self._model(**obj_in_data)
#         db.add(db_obj)
#         await db.commit()
#         await db.refresh(db_obj)
#         return db_obj
#
#     async def update(self, db: AsyncSession, *, db_obj: ModelType, obj_in) -> ModelType:
#         db_obj = await self.get(db=db, id=db_obj)
#         await db.commit()
#         await db.refresh(db_obj)
#         return jsonable_encoder(db_obj)
#
#     async def delete(self, db: AsyncSession, *, id: int) -> ModelType | None:
#         db_obj = await self.get(db=db, id=id)
#         await db.delete(db_obj)
#         await db.commit()
#         return db_obj
