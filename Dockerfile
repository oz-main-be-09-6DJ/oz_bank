# 베이스 이미지 (본인 프로젝트에 맞는 버전 기입)
FROM python:3.13-slim

ENV PYTHONPATH=/oz_bank
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# 종속성 파일 복사
COPY ./poetry.lock /oz_bank/
COPY ./pyproject.toml /oz_bank/
#COPY ./poetry.lock ./pyproject.toml ./

# 작업 디렉토리 설정
WORKDIR /oz_bank

# 필수 시스템 패키지 설치
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# 종속성 설치
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root
RUN poetry add gunicorn

# 애플리케이션 코드 복사
COPY ./apps /oz_bank/apps
WORKDIR /oz_bank/apps

# 소켓 파일 생성 디렉토리 권한 설정
RUN mkdir -p /oz_bank && chmod -R 755 /oz_bank

# 기존 코드: 직접 gunicorn 사용해서 실행
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]

# 변경된 코드: 스크립트를 사용하여 애플리케이션 실행
#COPY ./scripts /scripts
#RUN chmod +x /scripts/run.sh
#CMD ["/scripts/run.sh"]
