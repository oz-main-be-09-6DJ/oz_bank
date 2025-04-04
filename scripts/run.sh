#!/bin/sh
set -e
python manage.py migrate # 실행 전에 migrate 자동실행
gunicorn --bind 0.0.0.0:8000 config.wsgi:application --workers 2