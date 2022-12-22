from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import ORJSONResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_session
from schemas import url as url_schema
from services.base import urls_crud
from core.config import logger

router = APIRouter()


@router.post('/urls', response_model=url_schema.UrlShort, status_code=status.HTTP_201_CREATED)
async def create_url(*, db: AsyncSession = Depends(get_session), url_in: url_schema.UrlCreate) -> any:
    logger.info(f'router create_url: {url_in}')
    url = await urls_crud.create(db=db, obj_url=url_in)
    return url


@router.get('/{url_id}', response_class=RedirectResponse)
async def get_url(*, db: AsyncSession = Depends(get_session), url_id: int) -> any:
    logger.info(f'router create_url: {url_id}')
    url = await urls_crud.get(db=db, url_id=url_id)
    logger.info(f'router create_url: {url}')
    if not url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found')
    return RedirectResponse(url=url.original_url)


@router.delete('/{url_id}/delete', status_code=status.HTTP_200_OK)
async def delete_url(*, db: AsyncSession = Depends(get_session), url_id: int) -> any:
    url = await urls_crud.delete(db=db, url_id=url_id)
    logger.info(f'router delete_url: {url_id}')
    if not url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found')
    return url


# @router.get('/urls/{url_id}/status')
# async def get_status(*, db: AsyncSession = Depends(get_session), url_id) -> any:
#     url_status = await urls_crud.get_status(db=db, url_id=url_id)
#     if not url_status:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
#         )
#     return ORJSONResponse(url_status)
