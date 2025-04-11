from main import fetch_
from time import sleep
from dotenv import load_dotenv
from os import environ as env
load_dotenv()

while True:
    fetch_()
    sleep(int(env.get('SCRAPE_TIMEOUT', 180)))