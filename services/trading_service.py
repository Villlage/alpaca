import alpaca_trade_api as tradeapi
from app import app, config 

api = tradeapi.REST(key_id=config.ALPACA_API_KEY, secret_key=config.ALPACA_SECRET_KEY, api_version='v2', base_url=config.ALPCA_API_BASE_URL)

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

	return res



def close_position(symbol:str):
	# Close a position altogther
	position = api.close_position(symbol)

	return position
