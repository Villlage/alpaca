# type: ignore
import pytest
from copy import copy
from common.exceptions import ValidationError

from tests.mocks.plaid_response import accounts_response, base_metadata
from third_party.plaid.plaid_client import get_access_token, get_plaid_accounts


class TestPlaidClient:
    @pytest.fixture()
    def accounts_payload(self):
        payload = copy(base_metadata)
        return payload

    @pytest.fixture()
    def mock_get_access(self, mocker):
        return mocker.patch(
            "third_party.plaid.plaid_client.client.Item.public_token.exchange",
            return_value=dict(access_token="exchanged_token", item_id="abc-123"),
        )

    @pytest.fixture()
    def mock_get_accounts(self, mocker):
        return mocker.patch(
            "third_party.plaid.plaid_client.client.Accounts.get",
            return_value=accounts_response,
        )

    def test_get_access_token(self, mock_get_access) -> None:
        exchnaged_token = get_access_token(public_token="token")

        assert exchnaged_token == "exchanged_token"
        mock_get_access.assert_called_once()

    def test_get_bad_access_token(self, mock_get_access) -> None:
        with pytest.raises(ValidationError):
            get_access_token("")

        mock_get_access.assert_not_called()

    def test_get_plaid_accounts(self, mock_get_accounts) -> None:
        res = get_plaid_accounts("test_token")
        assert res == accounts_response

        mock_get_accounts.assert_called_once()
