import asyncio

from aiohttp.client import ClientSession
from dotenv import load_dotenv
from os import environ as env
from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync
from influxdb_client import Point

load_dotenv()

import shlex
from subprocess import Popen, PIPE, STDOUT
from pyping_py3 import ping, UnknownHostError

def get_ping_time(host):
    try:
        return ping(host, udp=True).avg_rtt
    except UnknownHostError:
        return -1


async def fetch():
    client = InfluxDBClientAsync(url=env.get('INFLUXDB_URL'), token=env.get('INFLUXDB_TOKEN'),
                                 org=env.get('INFLUXDB_ORG'))
    write_api, query_api = client.write_api(), client.query_api()

    sess = ClientSession()
    resp = await sess.get('https://station14.ru/favicon.ico')
    status_point = (Point("status_probe")
                    .tag('status', 'ok' if resp.ok else 'err')
                    .field('status_code', resp.status))

    ping_ms = get_ping_time('station14.ru')
    ping_point = (Point("ping_probe")
                  .tag('status', 'ok' if ping_ms != -1 else 'err')
                  .field('ping', ping_ms))

    await write_api.write(bucket=env.get('INFLUXDB_BUCKET'), org=env.get('INFLUXDB_ORG'), record=status_point)
    await write_api.write(bucket=env.get('INFLUXDB_BUCKET'), org=env.get('INFLUXDB_ORG'), record=ping_point)
    resp.close()
    await sess.close()

def fetch_():
    asyncio.run(fetch())
