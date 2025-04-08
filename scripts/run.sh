#!/bin/bash
set -e
export DJANGO_SETTINGS_MODULE=config.settings.prod
cd /oz_bank/apps
python manage.py migrate # 실행 전에 migrate 자동실행
gunicorn --bind 0.0.0.0:8000 config.wsgi:application --workers 2