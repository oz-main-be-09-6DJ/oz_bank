#!/bin/sh
set -e

# 설정을 명확히 설정
export DJANGO_SETTINGS_MODULE=config.settings.prod

# manage.py 위치로 이동
cd /oz_bank/apps

# 마이그레이션 수행
python manage.py migrate

# 서버 실행
gunicorn --bind 0.0.0.0:8000 config.wsgi:application --workers 2
