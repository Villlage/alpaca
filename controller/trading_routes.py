import requests
from flask import jsonify, Response, request
from typing import Tuple
import json 

from app import app
from controller.common import login_required

API_KEY = 'your-alpaca-api-key'
SECRET_KEY = 'your-alpaca-secret-key'
BASE_URL = "https://paper-api.alpaca.markets"
ORDERS_URL = "{}/v2/orders".format(BASE_URL)
HEADERS = {'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': SECRET_KEY}


@app.route('/trade', methods=['POST'])
def trade():
    webhook_message = request.json

    data = {
        "symbol": webhook_message['ticker'],
        "qty": 1,
        "side": "buy",
        "type": "limit",
        "limit_price": webhook_message['close'],
        "time_in_force": "gtc",
        "order_class": "bracket",
        "take_profit": {
            "limit_price": webhook_message['close'] * 1.05
        },
        "stop_loss": {
            "stop_price": webhook_message['close'] * 0.98,
        }
    }
    response = requests.post(ORDERS_URL, json=data, headers=HEADERS)

    return {
        'webhook_message': webhook_message,
        'id': response['id'],
        'client_order_id': response['client_order_id']
    }


@app.route('/status', methods=['GET'])
def status():
    return {
        'message': 'hello',
    }


