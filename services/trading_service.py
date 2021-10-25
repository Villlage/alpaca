import math
from typing import List
import alpaca_trade_api as tradeapi
from app import app, config, PRODUCTION, TESTING, STAGING, DEVELOPMENT, logger
import telebot

api = tradeapi.REST(key_id=config.ALPACA_API_KEY, secret_key=config.ALPACA_SECRET_KEY, api_version='v2', base_url=config.ALPCA_API_BASE_URL)
telgram_bot = telebot.TeleBot(config.TELEGRAM_KEY)

def send_message(text) -> None:
    if app.env == DEVELOPMENT:
        return None

    if app.env in [STAGING, TESTING]:
        text = f"{app.env}: " + text

    telgram_bot.send_message(text=text, chat_id=505895394)

def get_postitions():
    # Get our position in AAPL example: 
    # aapl_position = api.get_position('AAPL')

    # Get a list of all of our positions.
    positions_arr = []
    portfolio = api.list_positions()

    # Print the quantity of shares for each position.
    for position in portfolio:
        positions_arr.append(f"{position.qty} shares of {position.symbol}")

    return positions_arr


def buy_stock(symbol:str, qty:float=1.0):
    # Submit a market order to buy a stock
    res = api.submit_order(
        symbol=symbol,
        qty=qty,
        side='buy',
        type='market',
        time_in_force='gtc'
    )
    send_message(text=f"I bought {qty} shares of {symbol}")

    return res

def get_asset(symbol: str):
    try: 
        res = api.get_asset(symbol)
        return res
    except Exception as error:
        logger.error(error)


def get_last_quote(symbol: str):
    try: 
        res = api.get_last_quote(symbol)
        return res
    except Exception as error:
        logger.error(error)


def get_last_trade(symbol: str):
    try: 
        res = api.get_last_trade(symbol)
        return res
    except Exception as error:
        logger.error(error)


def buy_fractional_stock(symbol:str, dollar_amount:float):
    """
    check if we can but the asset and it's fractionable.
    If not, buy it regularly
    """
    try: 
        asset = get_asset(symbol)
        
        trade = get_last_trade(symbol)
        price = trade.price

        if not asset.fractionable:
            if price > dollar_amount or price == 0:
                logger.error(f"Price {price} is more than the dollar amount {dollar_amount}, but we can't buy the stock in fractions")
                return None

            quantity = math.floor(dollar_amount / price) or 1 
            res = buy_stock(symbol, quantity)
        else:
            res = buy_fractional_stock_api(symbol=symbol, dollar_amount=dollar_amount)        

        return res
    except Exception as error:
        logger.error(error)



def buy_fractional_stock_api(symbol:str, dollar_amount:float):
    # Submit a market order to buy a stock
    try: 
        res = api.submit_order(
            symbol=symbol,
            notional=dollar_amount,
            side='buy',
            type='market',
            time_in_force='day'
        )
    except Exception as error:
        print("something")


    send_message(text=f'I bought ${dollar_amount} of {symbol}')

    return res


def sell_stock(symbol:str, qty:float=1.0):
    # Submit a market order to sell a stock
    res = api.submit_order(
        symbol=symbol,
        qty=qty,
        side='sell',
        type='market',
        time_in_force='gtc',
    )

    send_message(text=f'I sold {qty} shares of {symbol}')

    return res



def close_position(symbol:str):
    # Close a position altogther
    try:
        position = api.close_position(symbol)
        send_message(text=f'I closed {symbol}. Quack')
    except Exception as error:
        send_message(text=f'I tried closing {symbol} but there is none')
    
    return position


def parse_stocks_email(text:str):
    import re
    stocks = []  
    all_stocks_text = re.findall('\nCheck out the following new tickers(.*)', text)
    texstush = all_stocks_text[0][1:].strip().split(', ')
    for stock_text in texstush:
        text_with_stock_name = stock_text.split(' ')[0].split(':')[1]
        stocks.append(text_with_stock_name)
    return stocks


def buy_stocks(stocks:List[str], dollar_amount:float):
    for stock in stocks:
        try:
            buy_fractional_stock(symbol=stock, dollar_amount=dollar_amount)
        except Exception as error:
            logger.error(error)


