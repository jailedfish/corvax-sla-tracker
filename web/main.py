import json

import ago
import requests
from flask import Flask, request, render_template
from influxdb_client.client.influxdb_client import InfluxDBClient
from dotenv import load_dotenv
from os import environ as env
from datetime import datetime, timedelta

load_dotenv()

app = Flask(__name__, template_folder='templates', static_folder='static')
client = InfluxDBClient(url=env.get('INFLUXDB_URL'), token=env.get('INFLUXDB_TOKEN'),
                                 org=env.get('INFLUXDB_ORG'))
query_api = client.query_api()


def get_stats() -> dict[str, int|str]:
    ping_query = '''
    import "array"
    get_sla = (d) => {
        all_requests = from(bucket: "main")
                |> range(start: d)
                |> filter(fn: (r) => r._measurement == "status_probe")
        
        total = all_requests
                |> count()
                |> toFloat()
                |> findRecord(fn: (key) => true, idx: 0)
        
        success = all_requests
                |> filter(fn: (r) => r._value == 200)
                |> count()
                |> toFloat()
                |> findRecord(fn: (key) => true, idx: 0)
        first_metric = all_requests 
                |> first()
                |> keep(columns: ["_time"])
                |> findRecord(fn: (key) => true, idx: 0)
        resp = {
            sla: (success._value) / total._value * 100.0,
            first_metric: first_metric._time
        }
        
        return resp 
    }
    ping = from(bucket: "main")
                |> range(start: -6h)
                |> filter(fn: (r) => r._measurement == "ping_probe")
                |> toFloat()
                |> findRecord(fn: (key) => true, idx: 0)  
    
    slaRecord = {
        time: now(),
        sla_daily: get_sla(d: -1d).sla,
        sla_monthly: get_sla(d: -1mo).sla,
        sla_yearly: get_sla(d: -1y).sla,
        first_metric_month: get_sla(d: -1mo).first_metric,
        first_metric_year: get_sla(d: -1y).first_metric,
        ping: ping._value,
        status: ping.status
    }
    array.from(rows: [slaRecord])
    '''
    res = query_api.query(ping_query)
    return json.loads(res.to_json())[0]

def get_ss14_stats():
    result = []
    try:
        servers = requests.get('https://hub.spacestation14.com/api/servers').json()
        for server in servers:
            print(server)
            if 'corvax' in server['statusData'].get('name', '').lower():
                corvax_host = server['statusData']

                buf = {'max_players': corvax_host.get('soft_max_players', 100),
                       'player_count': corvax_host.get('players', -1),
                       'round_time': ago.human(
                            datetime.now() - datetime.fromisoformat(corvax_host.get('round_start_time',
                                                                    datetime.now().isoformat()).replace('Z', '+00:00'))
                                                                    .replace(tzinfo=None)),
                       'preset': corvax_host.get('preset', 'Секрет'),
                       'name': corvax_host.get('name', ''), 'map': corvax_host.get('map', 'unknown')}

                result.append(buf)
    except Exception as e:
        print(e)
    finally:
        return result


@app.get('/')
def get_index():
    stats = get_stats()
    c_stats = get_ss14_stats()
    return render_template('index.html',
                           is_up=stats.get('status', 'err') == 'ok',
                           daily_uptime=stats.get('sla_daily', 100),
                           monthly_uptime=stats.get('sla_monthly', 100),
                           yearly_uptime=stats.get('sla_yearly', 100),
                           ping=stats.get('ping', 10),
                           first_metric_month=ago.human(datetime.fromisoformat(stats.get('first_metric_year', datetime.now()))),
                           first_metric_year=ago.human(datetime.fromisoformat(stats.get('first_metric_year', datetime.now()))),
                           servers=c_stats)



def main():
    app.run('0.0.0.0', 8081, env.get('DEBUG', False))

main()