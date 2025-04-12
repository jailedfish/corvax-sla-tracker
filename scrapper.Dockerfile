FROM python:3.12

WORKDIR /app

RUN [ "pip", "install", "--no-cache-dir", "influxdb-client", "python-dotenv", "pyping", "jinja2", "flask", "aiohttp", "ago", "pyping-py3==0.1.0" ]
RUN [ "apt", "update", "-y"]
RUN [ "apt", "install", "-y", "fping" ]

COPY scrapper/ /app
COPY .env /app
ENTRYPOINT [ "python", "docker-loop.py" ]