import os
from logging import config, getLogger

from pydantic import BaseSettings, PostgresDsn

from core.logger import LOGGING


class AppSettings(BaseSettings):
    app_title: str = 'LibraryApp'
    database_dsn: PostgresDsn

    class Config:
        env_file = '.env'
        BLOCKED_IPS = []


app_settings = AppSettings()
# Применяем настройки логирования
config.dictConfig(LOGGING)
logger = getLogger(__name__)

# Название проекта. Используется в Swagger-документации
PROJECT_NAME = os.getenv('PROJECT_NAME', 'library')
PROJECT_HOST = os.getenv('PROJECT_HOST', '0.0.0.0')
PROJECT_PORT = int(os.getenv('PROJECT_PORT', '8000'))

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
