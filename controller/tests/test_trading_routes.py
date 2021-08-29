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
            assert resp.json['message'] == 'hello'
