FROM python:3.12

WORKDIR /app

RUN [ "pip", "install", "--no-cache-dir", "influxdb-client", "python-dotenv", "pyping", "jinja2", "flask", "aiohttp", "ago" ]
RUN [ "apt", "update", "-y"]
RUN [ "apt", "install", "-y", "fping" ]

COPY scrapper/ /app
COPY .env /app
ENTRYPOINT [ "python", "docker-loop.py" ]