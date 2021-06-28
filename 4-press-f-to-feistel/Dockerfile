FROM python:3.8-alpine

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /app
WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY ./service/ /app/

CMD [ "gunicorn", "-b", "0.0.0.0:8080", "-w", "4", "main:app" ]