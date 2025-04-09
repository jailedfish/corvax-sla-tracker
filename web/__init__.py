from flask import Flask, request, render_template
from jinja2 import Environment, FileSystemLoader
from influxdb_client.client.influxdb_client import InfluxDBClient
from dotenv import load_dotenv
from os import environ as env
load_dotenv()

app = Flask(__name__, template_folder='templates')

client = InfluxDBClient(url=env.get('INFLUXDB_URL'), token=env.get('INFLUXDB_TOKEN'),
                                 org=env.get('INFLUXDB_ORG'))
query_api = client.query_api()


def get_stats():
    query = '''
    from(bucket: "main")
      |> range(start: -1h)
      |> filter (fn: (r) => r._measurement == "ping_probe")
      |> mean()
    '''
    res = query_api.query(query)
    print(res)


@app.get('/')
def get_index():
    get_stats()
    return render_template('index.html', is_up=True, daily_uptime=100, monthly_uptime=0, ping=10)


def main():
    app.run('0.0.0.0', 8080, True)

main()