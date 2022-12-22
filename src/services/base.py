# from models.user import User as UserModel
# from schemas.user import UserCreate, UserUpdate
#
# from .user import RepositoryDB as UserRepositoryDB
#
#
# class RepositoryUser(UserRepositoryDB[UserModel, UserCreate, UserUpdate]):
#     pass
#
#
# user_crud = RepositoryUser(UserModel)

from models.url import ShortUrl
from schemas.url import UrlCreate

from .url import RepositoryDB


class RepositoryURL(RepositoryDB[ShortUrl, UrlCreate]):
    pass


urls_crud = RepositoryURL(ShortUrl)
