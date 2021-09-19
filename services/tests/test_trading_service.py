# type: ignore
import pytest
from tests.factories import faker, UserFactory
from services.trading_service import buy_stock, sell_stock, get_postitions
from unittest.mock import MagicMock

class TestBuySell:
    @pytest.fixture()
    def mock_alpaca_api(self, mocker) -> None:
        return mocker.patch(
            "services.trading_service.api.submit_order",
            return_value="",
        )

    def test_buy_stock(self, mock_alpaca_api) -> None:
        symbol = "AAPL"
        qty = 3.2
        res = buy_stock(symbol=symbol, qty=qty)
        assert res == ""

    def test_sell_stock(self, mock_alpaca_api) -> None:
        symbol = "AAPL"
        qty = 3.1
        res = sell_stock(symbol=symbol, qty=qty)
        assert res == ""

class TestPortfolio:
    @pytest.fixture()
    def mock_alpaca_api(self, mocker) -> None:
        return mocker.patch(
            "services.trading_service.api.list_positions",
            return_value=[MagicMock(qty=1.0, symbol="AAPL")]
        )

    def test_get_postitions(self, mock_alpaca_api):
        res = get_postitions()
        assert res == ["1.0 shares of AAPL"]