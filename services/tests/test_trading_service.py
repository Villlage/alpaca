# type: ignore
import pytest
from tests.factories import faker, UserFactory
from services.trading_service import buy_stock, sell_stock, get_postitions, close_position, buy_fractional_stock, parse_stocks_email, get_asset, get_last_quote, get_last_trade, buy_fractional_stock_api
from unittest.mock import MagicMock


@pytest.fixture()
def mock_telegram_api(mocker) -> None:
    return mocker.patch(
        "services.trading_service.telebot.TeleBot.send_message",
        return_value="",
    )


@pytest.fixture()
def mock_alpaca_api_get_asset(mocker) -> None:
    return mocker.patch(
        "services.trading_service.api.get_asset",
        return_value=MagicMock(fractionable=True),
    )


@pytest.fixture()
def mock_alpaca_api_get_asset_fractionable_false(mocker) -> None:
    return mocker.patch(
        "services.trading_service.api.get_asset",
        return_value=MagicMock(fractionable=False),
    )

@pytest.fixture()
def mock_alpaca_api_last_quote(mocker) -> None:
    return mocker.patch(
        "services.trading_service.api.get_last_quote",
        return_value=MagicMock(price=12.0),
    )

@pytest.fixture()
def mock_alpaca_api_last_trade(mocker) -> None:
    return mocker.patch(
        "services.trading_service.api.get_last_trade",
        return_value=MagicMock(price=12.0),
    )

@pytest.fixture()
def mock_alpaca_api(mocker) -> None:
    return mocker.patch(
        "services.trading_service.api.submit_order",
        return_value="",
    )


class TestBuySell:
    def test_buy_stock(self, mock_alpaca_api, mock_telegram_api) -> None:
        symbol = "AAPL"
        qty = 3.2
        res = buy_stock(symbol=symbol, qty=qty)
        assert res == ""
        mock_alpaca_api.assert_called_once()
        mock_telegram_api.assert_called_once()

    def test_sell_stock(self, mock_alpaca_api, mock_telegram_api) -> None:
        symbol = "AAPL"
        qty = 3.1
        res = sell_stock(symbol=symbol, qty=qty)
        assert res == ""
        mock_alpaca_api.assert_called_once()
        mock_telegram_api.assert_called_once()

    def test_buy_fractional_stock_api(self, mock_alpaca_api, mock_telegram_api) -> None:
        symbol = "AAPL"
        dollar_amount = 30.0
        res = buy_fractional_stock_api(symbol=symbol, dollar_amount=dollar_amount)
        assert res == ""
        mock_alpaca_api.assert_called_once()
        mock_telegram_api.assert_called_once()


class TestAPI:
    def test_get_asset(self, mock_alpaca_api_get_asset):
        res = get_asset(symbol="AAPL")
        mock_alpaca_api_get_asset.assert_called_once()

    def test_get_last_quote(self, mock_alpaca_api_last_quote):
        res = get_last_quote(symbol="AAPL")
        mock_alpaca_api_last_quote.assert_called_once()

    def test_get_last_trade(self, mock_alpaca_api_last_trade):
        res = get_last_trade(symbol="AAPL")
        mock_alpaca_api_last_trade.assert_called_once()


class TestBuyFractionalStock:
   def test_buy_fractional_stock(self, mock_alpaca_api, mock_alpaca_api_last_trade, mock_alpaca_api_get_asset, mock_telegram_api):
        res = buy_fractional_stock(symbol="AAPL", dollar_amount=20.1)
        mock_alpaca_api.assert_called_once()
        mock_alpaca_api_last_trade.assert_called_once()
        mock_alpaca_api_get_asset.assert_called_once()
        mock_telegram_api.assert_called_once()

   def test_buy_fractional_stock_not_fractionable(self, mock_alpaca_api, mock_alpaca_api_last_trade, mock_alpaca_api_get_asset_fractionable_false, mock_telegram_api):
        res = buy_fractional_stock(symbol="AAPL", dollar_amount=20.1)
        mock_alpaca_api.assert_called_once()
        mock_alpaca_api_last_trade.assert_called_once()
        mock_alpaca_api_get_asset_fractionable_false.assert_called_once()
        mock_telegram_api.assert_called_once()



class TestClosePosition:
    @pytest.fixture()
    def mock_alpaca_api(self, mocker) -> None:
        return mocker.patch(
            "services.trading_service.api.close_position",
            return_value="",
        )

    def test_close_position(self, mock_alpaca_api, mock_telegram_api) -> None:
        symbol = "AAPL"
        res = close_position(symbol=symbol)
        assert res == ""



class TestPortfolio:
    @pytest.fixture()
    def mock_alpaca_api(self, mocker) -> None:
        return mocker.patch(
            "services.trading_service.api.list_positions",
            return_value=[MagicMock(qty=1.0, symbol="AAPL")]
        )

    def test_get_postitions(self, mock_alpaca_api, mock_telegram_api) -> None:
        res = get_postitions()
        assert res == ["1.0 shares of AAPL"]

class TestEmail:
    def test_parsing_email(self):
        stocks = parse_stocks_email('New MACD\n\nCheck out the following new tickers: NASDAQ:BGFV ( https://www.tradingview.com/chart/?symbol=NASDAQ%3ABGFV ) , NASDAQ:CENT ( https://www.tradingview.com/chart/?symbol=NASDAQ%3ACENT ) , NASDAQ:CMRX ( https://www.tradingview.com/chart/?symbol=NASDAQ%3ACMRX ) , NASDAQ:CRSR ( https://www.tradingview.com/chart/?symbol=NASDAQ%3ACRSR ) , NYSE:ELF ( https://www.tradingview.com/chart/?symbol=NYSE%3AELF ) , NYSE:OLO ( https://www.tradingview.com/chart/?symbol=NYSE%3AOLO ) , NYSE:SHAK ( https://www.tradingview.com/chart/?symbol=NYSE%3ASHAK )')
        assert stocks == ['BGFV', 'CENT', 'CMRX', 'CRSR', 'ELF', 'OLO', 'SHAK']


