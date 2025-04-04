from .base import *

# DEBUG 설정 (개발 환경에서는 보통 True로 설정)
DEBUG = os.getenv("DEBUG", default=False)

ALLOWED_HOSTS = []

ROOT_URLCONF = 'apps.config.urls.urls_prod'

# DB연결 정보
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
    }
}