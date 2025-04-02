from .base import *

# DEBUG 설정 (개발 환경에서는 보통 True로 설정)
DEBUG = os.getenv("DEBUG", default=False)

ALLOWED_HOSTS = []

ROOT_URLCONF = 'config.urls.urls_prod'