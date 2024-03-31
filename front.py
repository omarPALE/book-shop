
from flask import Flask, jsonify, request
import requests
from urllib.parse import unquote

app = Flask(__name__)

CATALOG_SERVER_IP = "127.0.0.1"  # Replace with the actual IP address
CATALOG_SERVER_PORT = 8001
ORDER_SERVER_IP = "127.0.0.1"  # Replace with the actual IP address
ORDER_SERVER_PORT = 8002

@app.route('/search/<topic>', methods=['GET'])
def search(topic):
    topic = unquote(topic)
    response = requests.get(f"http://{CATALOG_SERVER_IP}:{CATALOG_SERVER_PORT}/query?topic={topic}")
    return response.json(), response.status_code

@app.route('/info/<int:item_number>', methods=['GET'])
def info(item_number):
    response = requests.get(f"http://{CATALOG_SERVER_IP}:{CATALOG_SERVER_PORT}/query/{item_number}")
    return response.json(), response.status_code

@app.route('/purchase/<int:item_number>', methods=['POST'])
def purchase(item_number):
    response = requests.post(f"http://{ORDER_SERVER_IP}:{ORDER_SERVER_PORT}/purchase/{item_number}")
    return response.json(), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
