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

from models.url import ShortUrl, User
from schemas.url import UrlCreate
from schemas.user import UserCreate

from .url import RepositoryDB as UrlDB
from .user import RepositoryDB as UserDB


class RepositoryURL(UrlDB[ShortUrl, UrlCreate]):
    pass


class RepositoryUser(UserDB[User, UserCreate]):
    pass


urls_crud = RepositoryURL(ShortUrl)
user_crud = RepositoryUser(User)
