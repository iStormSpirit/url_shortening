from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import ORJSONResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import logger
from db.db import get_session
from schemas import url as url_schema
from services.base import urls_crud

router = APIRouter()


@router.get('/ping', tags=['info'])
async def check_status_db(db: AsyncSession = Depends(get_session)):
    result = await urls_crud.get_ping_db(db=db)
    logger.info(f'ping for select query in db: {result}')
    return result


@router.post('/urls', response_model=url_schema.UrlShort, status_code=status.HTTP_201_CREATED)
async def create_url(*, db: AsyncSession = Depends(get_session), url_in: url_schema.UrlCreate) -> any:
    logger.info(f'router create_url: {url_in}')
    url = await urls_crud.create(db=db, obj_url=url_in)
    return url


@router.get('/{url_id}', response_class=RedirectResponse)
async def get_url(*, db: AsyncSession = Depends(get_session), url_id: int) -> any:
    logger.info(f'router create_url: {url_id}')
    url = await urls_crud.get_redirect(db=db, url_id=url_id)
    logger.info(f'router create_url: {url}')
    if not url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found')
    if url == 410:
        raise HTTPException(status_code=status.HTTP_410_GONE, detail='Gone')
    return RedirectResponse(url=url.original_url)


@router.delete('/{url_id}/delete', status_code=status.HTTP_200_OK)
async def archived_url(*, db: AsyncSession = Depends(get_session), url_id: int) -> any:
    url = await urls_crud.archived(db=db, url_id=url_id)
    logger.info(f'router delete_url: {url_id}')
    if not url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found')
    return url


@router.delete('/{url_id}/real_delete', status_code=status.HTTP_200_OK)
async def delete_url(*, db: AsyncSession = Depends(get_session), url_id: int) -> any:
    url = await urls_crud.delete(db=db, url_id=url_id)
    logger.info(f'router delete_url: {url_id}')
    if not url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found')
    return url


@router.get('/{url_id}/status', response_model=url_schema.UrlStatus)
async def get_url_status(*, db: AsyncSession = Depends(get_session), url_id: int) -> any:
    url = await urls_crud.get(db=db, url_id=url_id)
    if not url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    if url == 410:
        raise HTTPException(status_code=status.HTTP_410_GONE, detail='Gone')
    return url


@router.get('/get_full_info_url/{url_id}', response_model=url_schema.UrlInDBase, status_code=status.HTTP_200_OK,
            tags=['info'])
async def get_full_info_url(*, db: AsyncSession = Depends(get_session), url_id: int) -> any:
    logger.info(f'router create_url: {url_id}')
    url = await urls_crud.get(db=db, url_id=url_id)
    logger.info(f'router create_url: {url}')
    if not url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found')
    if url == 410:
        raise HTTPException(status_code=status.HTTP_410_GONE, detail='Gone')
    return url
