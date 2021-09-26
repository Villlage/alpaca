# type: ignore
import pytest
from tests.factories import faker, UserFactory
from services.trading_service import buy_stock, sell_stock, get_postitions, close_position, buy_fractional_stock
from unittest.mock import MagicMock

@pytest.fixture()
def mock_telegram_api(mocker) -> None:
    return mocker.patch(
        "services.trading_service.telebot.TeleBot.send_message",
        return_value="",
    )


class TestBuySell:
    @pytest.fixture()
    def mock_alpaca_api(self, mocker) -> None:
        return mocker.patch(
            "services.trading_service.api.submit_order",
            return_value="",
        )

    def test_buy_stock(self, mock_alpaca_api, mock_telegram_api) -> None:
        symbol = "AAPL"
        qty = 3.2
        res = buy_stock(symbol=symbol, qty=qty)
        assert res == ""

    def test_sell_stock(self, mock_alpaca_api, mock_telegram_api) -> None:
        symbol = "AAPL"
        qty = 3.1
        res = sell_stock(symbol=symbol, qty=qty)
        assert res == ""

    def test_buy_fractional_stock(self, mock_alpaca_api, mock_telegram_api) -> None:
        symbol = "AAPL"
        dollar_amount = 30.0
        res = buy_fractional_stock(symbol=symbol, dollar_amount=dollar_amount)
        assert res == ""


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
