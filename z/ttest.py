from typing import Any

from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import logger
from db.db import get_session
from schemas import user as user_schema
from services.base import user_crud

router = APIRouter()

from services.security import verify_password

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

app = FastAPI()


def fake_hash_password(password: str):
    logger.info(f'---------------------------- fake_hash_password get password{password}')
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    logger.info(f'---------------------------- get_user get db and  username {username}')
    if username in db:
        user_dict = db[username]
        logger.info(f'---------------------------- get_user get user_dict {user_dict}')
        logger.info(f'---------------------------- get_user return UserInDB {UserInDB(**user_dict)}')
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    logger.info(f'---------------------------- fake_decode_token get token{token}')
    user = get_user(fake_users_db, token)
    logger.info(f'---------------------------- fake_decode_token return {user}')
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    logger.info(f'---------------------------- get_current_user get token{token}')
    user = fake_decode_token(token)
    logger.info(f'---------------------------- get_current_user fake_decode_token{user}')
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    logger.info(f'---------------------------- get_current_user return {user}')
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    logger.info(f'---------------------------- get_current_active_user get current_user{current_user}')
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user