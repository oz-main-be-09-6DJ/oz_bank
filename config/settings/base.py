"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
import json
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta

# 프로젝트 루트 경로
BASE_DIR = Path(__file__).resolve().parent.parent.parent
print("BASE_DIR : ", BASE_DIR)

# secret.json 로드
SECRET = {}
secret_path = BASE_DIR / '.config_secret' / 'secret.json'

if secret_path.exists():
    try:
        with open(secret_path) as f:
            SECRET = json.load(f)
    except json.JSONDecodeError:
        print("⚠️ secret.json 파일이 있지만 JSON 형식이 올바르지 않습니다.")
else:
    print("⚠️ secret.json 파일이 존재하지 않습니다. 테스트 환경 또는 기본 설정이 사용됩니다.")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-&-0k^p0-7u@x*r3=7vi9eh7m=99e(o_tpos$!f_9a7cg)zbbz_'

# Django 기본 내장 앱들
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework_simplejwt.token_blacklist',
    'rest_framework_simplejwt',
    'rest_framework',
]

APP_APPS = [
    'users',
    'transaction',
    'analysis',
    'account',
    'core',
]

# Django에게 기본 User 모델 대신 CustomUser 사용하도록 설정
AUTH_USER_MODEL = 'users.CustomUser'

# 최종적으로 Django가 로드할 앱 리스트
INSTALLED_APPS = DJANGO_APPS + APP_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / 'templates' ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# 환경 변수 로드
load_dotenv()

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#from datetime import timedelta
SIMPLE_JWT={
    "ACCESS_TOKEN_LIFETIME":timedelta(days=7) #JWT토큰 만료 시간 7일
}

# OAuth (naver)
# secret.json이 없거나 키가 없을 경우를 대비
NAVER_CLIENT_ID = SECRET.get("naver", {}).get("client_id", "")
NAVER_SECRET = SECRET.get("naver", {}).get("secret", "")