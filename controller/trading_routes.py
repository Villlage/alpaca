import requests
from flask import jsonify, Response, request
from typing import Tuple
import json 

from app import app, config 
from controller.common import login_required

from services.trading_service import get_postitions, sell_stock, buy_stock

BASE_URL = "https://paper-api.alpaca.markets"
ORDERS_URL = "{}/v2/orders".format(BASE_URL)
HEADERS = {'APCA-API-KEY-ID': config.ALPACA_API_KEY, 'APCA-API-SECRET-KEY': config.ALPACA_SECRET_KEY}


@app.route('/trade', methods=['POST'])
def trade():
    """
    This route makes it possible to receive a webhook from:
    TradingView: https://www.tradingview.com/chart/8Vu3wN5S/

    Example for a webhook: 
    { "close": {{close}}, "volume": {{volume}} }
    """
    
    webhook_message = request.json
    webhook_message['ticker'] = "GOOG"

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
        'ALPACA_API_KEY': config.ALPACA_API_KEY,
        'message': 'Operational I am',
    }


@app.route('/buy', methods=['POST'])
def buy():
    webhook_message = request.json
    symbol = str(webhook_message['ticker'])
    response = buy_stock(symbol, qty=1.0)
    return jsonify(response), 200

@app.route('/sell', methods=['POST'])
def sell():
    webhook_message = request.json
    symbol = str(webhook_message['ticker'])
    response = sell_stock(symbol, qty=1.0)
    return jsonify(response), 200


@app.route('/portfolio', methods=['GET'])
def portfolio():
    postitions = get_postitions()
    return jsonify(postitions), 200
