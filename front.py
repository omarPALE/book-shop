from flask import Flask, jsonify, request
import requests
from urllib.parse import unquote

app = Flask(__name__)

CATALOG_SERVER_URL = "http://catalog-server:5001"
ORDER_SERVER_URL = "http://order-server:5002"

@app.route('/search', methods=['GET'])
def search():
    topic = request.args.get('topic')
    if topic:
        topic = unquote(topic)  # Decode URL-encoded parameter
    else:
        # Handle case when 'topic' parameter is not provided
        return jsonify({'error': 'Topic parameter is required'}), 400
    response = requests.get(f"{CATALOG_SERVER_URL}/query?topic={topic}")
    return response.json(), response.status_code

@app.route('/info/<int:item_number>', methods=['GET'])
def info(item_number):
    response = requests.get(f"{CATALOG_SERVER_URL}/query/{item_number}")
    return response.json(), response.status_code

@app.route('/purchase/<int:item_number>', methods=['POST'])
def purchase(item_number):
    response = requests.post(f"{ORDER_SERVER_URL}/purchase/{item_number}")
    return response.json(), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
