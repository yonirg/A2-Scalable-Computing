import requests
from server import *
import json
import time


def consume_webhook():
    url = "http://127.0.0.1:5000/data"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        for record in data:
            extra_1 = record["extra_1"]
            if extra_1 == "SCROLLING":
                process_scrolling_data.delay(json.dumps(record))
            elif extra_1 == "ZOOM":
                process_zoom_data.delay(json.dumps(record))
            elif extra_1 == "CLICK":
                process_click_data.delay(json.dumps(record))
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")

if __name__ == "__main__":
    start_time = time.time()
    consume_webhook()
    end_time = time.time() - start_time
    print(f"Tempo de operação: {end_time} segundos")