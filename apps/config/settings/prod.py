from .base import *
import certifi
# DEBUG 설정 (개발 환경에서는 보통 True로 설정)
DEBUG = os.getenv("DEBUG", default=False)
#os.environ['SSL_CERT_FILE'] = certifi.where() 
ALLOWED_HOSTS = ['127.0.0.1']

ROOT_URLCONF = 'config.urls.urls_prod'
# DATABASES 설정을 환경 변수로부터 가져오기
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "5432"),
        "NAME": os.getenv("DB_NAME", "django"),
        "USER": os.getenv("DB_USER", "postgres"),
        "PASSWORD": os.getenv("DB_PASSWORD", "postgres"),
    }
}
# Email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.naver.com"
EMAIL_USE_TLS = True    # 보안 연결(TLS)용으로 EMAIL_PORT 연결과 관련
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv("USER_ID")
EMAIL_HOST_PASSWORD = os.getenv("PASSWORD")
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'PAGE_SIZE':10,
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'DEFAULT_AUTHENTICATION_CLASSES':[
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

STATIC_URL = f'https://{os.getenv("S3_STORAGE_BUCKET_NAME", "django-mini-project")}.s3.amazonaws.com/static/'
MEDIA_URL = f'https://{os.getenv("S3_STORAGE_BUCKET_NAME", "django-mini-project")}.s3.amazonaws.com/media/'

# STORAGES 작성
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "access_key": os.getenv("S3_ACCESS_KEY", ""),
            "secret_key": os.getenv("S3_SECRET_ACCESS_KEY", ""),
            "bucket_name": os.getenv("S3_STORAGE_BUCKET_NAME", ""),
            "region_name": os.getenv("S3_REGION_NAME", ""),
            "location": "media",
            "default_acl": "public-read",
        },
    },
    "staticfiles": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "access_key": os.getenv("S3_ACCESS_KEY", ""),
            "secret_key": os.getenv("S3_SECRET_ACCESS_KEY", ""),
            "bucket_name": os.getenv("S3_STORAGE_BUCKET_NAME", ""),
            "region_name": os.getenv("S3_REGION_NAME", ""),
            "custom_domain": f'{os.getenv("S3_STORAGE_BUCKET_NAME", "")}.s3.amazonaws.com',
            "location": "static",
            "default_acl": "public-read",
        },
    },
}