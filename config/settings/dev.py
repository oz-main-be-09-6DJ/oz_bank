from .base import *

# DEBUG 설정 (개발 환경에서는 보통 True로 설정)
DEBUG = os.getenv("DEBUG", default=True)

ALLOWED_HOSTS = []

# DATABASES 설정을 환경 변수로부터 가져오기
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", default="postgres"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("DB_HOST", default="localhost"),
        "PORT": os.getenv("DB_PORT", default="5432"),
    }
}

ROOT_URLCONF = 'config.urls.urls_dev'

# drf_spectacular.openapi.AutoSchema: 자동으로 OpenAPI(Swagger) 문서를 생성할 수 있게 해준다.
# 즉, drf-spectacular이 DRF의 API 엔드포인트를 분석하여 Swagger 문서를 생성할 수 있도록 해준다.
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'PAGE_SIZE':10,
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'DEFAULT_AUTHENTICATION_CLASSES':[
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ]
}