# type: ignore
import pytest
from app import app
import json

class TestTradeRoutes:
    @pytest.fixture()
    def mock_posting_alpaca(self, mocker) -> None:
        return mocker.patch(
            "requests.post",
            return_value=dict(client_order_id=14,id=14434),
        )

    def test_trade_post_webhook(self, mock_posting_alpaca):
        with app.test_client() as client:
            resp = client.post(
                "/trade",
                data=json.dumps(dict(ticker="AAPL", close=123)),
                content_type="application/json",
            )

            assert resp.status_code == 200
            assert resp.json['client_order_id'] == 14
            assert mock_posting_alpaca.call_count == 1

    def test_status(self):
        with app.test_client() as client:
            resp = client.get("/status")

            assert resp.status_code == 200
            assert resp.json['message'] == 'Operational I am'


class TestBuy:
    @pytest.fixture()
    def mock_buy_stock(self, mocker) -> None:
        return mocker.patch(
            "controller.trading_routes.buy_stock",
            return_value="",
        )

    def test_buy_stock(self, mock_buy_stock):
        with app.test_client() as client:
            resp = client.post(
                "/buy",
                data=json.dumps(dict(ticker="GOOG", close=123)),
                content_type="application/json",
            )

            assert resp.status_code == 200


class TestSell:
    @pytest.fixture()
    def mock_sell_stock(self, mocker) -> None:
        return mocker.patch(
            "controller.trading_routes.sell_stock",
            return_value="",
        )

    def test_sell_stock(self, mock_sell_stock):
        with app.test_client() as client:
            resp = client.post(
                "/sell",
                data=json.dumps(dict(ticker="GOOG", close=123)),
                content_type="application/json",
            )

            assert resp.status_code == 200

class TestPortfolio:
    @pytest.fixture()
    def mock_portfolio(self, mocker) -> None:
        return mocker.patch(
            "controller.trading_routes.get_postitions",
            return_value=[{'AAPL':123}, {'GOOG':321}],
        )

    def test_portfolio(self, mock_portfolio):
        with app.test_client() as client:
            resp = client.get("/portfolio")

            assert resp.status_code == 200
            assert resp.json == [{'AAPL':123}, {'GOOG':321}]

