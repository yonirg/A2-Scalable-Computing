import requests

def consume_webhook():
    url = "http://127.0.0.1:5000/data"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        for record in data:
            print(record)
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")

if __name__ == "__main__":
    consume_webhook()
