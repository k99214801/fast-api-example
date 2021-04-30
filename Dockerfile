FROM python:3.9-slim

ENV LANG ko_KR.utf-8
ENV PYTHONUNBUFFERED 1

RUN set -ex \
    && ln -s -f /usr/share/zoneinfo/Asia/Seoul /etc/localtime

RUN set -ex \
    && apt-get update \
    && apt-get -y install gcc g++ nginx libmariadb-dev procps libcurl4-openssl-dev libssl-dev

WORKDIR /app

COPY . .

RUN set -ex \
    && pip install -r requirements/base.txt

CMD ["uvicorn", "server:create_app", "--host", "0.0.0.0", "--port", "80"]