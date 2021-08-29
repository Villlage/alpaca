# type: ignore
import pytest
from copy import copy
from tests.factories import UserFactory
from services.plaid_service import create_plaid_item

from tests.mocks.plaid_response import accounts_response, base_metadata


class TestPlaidCreate:
    @pytest.fixture()
    def accounts_payload(self) -> None:
        payload = copy(base_metadata)
        payload["accounts"] = accounts_response["accounts"]
        return payload

    @pytest.fixture()
    def mock_get_access(self, mocker) -> None:
        return mocker.patch(
            "services.plaid_service.get_access_token", return_value="test_token",
        )

    @pytest.fixture()
    def mock_get_accounts(self, mocker) -> None:
        return mocker.patch(
            "third_party.plaid.plaid_client.client.Accounts.get",
            return_value=accounts_response,
        )

    def test_create_plaid_item(
        self, accounts_payload, mock_get_access, mock_get_accounts
    ) -> None:
        user = UserFactory.create()
        public_token = "test"
        plaid_item = create_plaid_item(
            user=user, public_token=public_token, metadata=accounts_payload
        )
        assert plaid_item
        assert plaid_item.user_id == user.id
        assert len(plaid_item.plaid_accounts) == 3
        assert sum([pa.current_balance for pa in plaid_item.plaid_accounts]) == 1020
