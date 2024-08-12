FROM python:3.8-slim

ARG SERVICE=login.py
ARG HOST=localhost

WORKDIR /usr/src/app

COPY ./services/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./services .

ENV SERVICE=$SERVICE
ENV HOST=$HOST

CMD python -u $SERVICE