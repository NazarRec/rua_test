FROM python:3.9.13 as base

COPY requirements.txt .

RUN pip3 install -r requirements.txt

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.7.2/wait /wait

RUN chmod +x /wait

FROM base as app

ARG SERVICE_NAME

COPY /${SERVICE_NAME} ./app/

CMD python3 /app/app.py