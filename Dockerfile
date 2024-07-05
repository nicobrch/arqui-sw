FROM python:3.8-alpine

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 5000

CMD tail -f /dev/null