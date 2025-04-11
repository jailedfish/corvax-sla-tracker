FROM python:3.12

WORKDIR /app

RUN [ "pip", "install", "--no-cache-dir", "influxdb-client", "python-dotenv", "jinja2", "flask", "ago" ]


COPY web/ /app
COPY .env /app

ENTRYPOINT [ "python", "main.py" ]