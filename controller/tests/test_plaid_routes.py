# type: ignore
import pytest
from copy import copy
import json
from tests.factories import PlaidItemFactory, UserFactory
from conftest import logged_in_client


from tests.mocks.plaid_response import accounts_response, base_metadata


class TestPlaidItem:
    @pytest.fixture()
    def accounts_payload(self):
        payload = copy(base_metadata)
        payload["accounts"] = accounts_response["accounts"]
        return payload

    @pytest.fixture()
    def mock_get_access(self, mocker):
        return mocker.patch(
            "services.plaid_service.get_access_token", return_value="test_token",
        )

    @pytest.fixture()
    def mock_get_accounts(self, mocker) -> None:
        return mocker.patch(
            "third_party.plaid.plaid_client.client.Accounts.get",
            return_value=accounts_response,
        )

    def test_post(self, accounts_payload, mock_get_access, mock_get_accounts) -> None:
        user = UserFactory.create()
        with logged_in_client(user) as client:
            resp = client.post(
                "/plaid/items",
                data=json.dumps(dict(public_token="test", metadata=accounts_payload)),
                content_type="application/json",
            )
            assert resp.status_code == 200
            assert resp.json["institution_name"] == "test_institution"
            assert resp.json["institution_id"] == "ins_109508"
            assert resp.json["user_id"] == user.id
            assert len(resp.json["plaid_accounts"]) == 3

    def test_get(self) -> None:
        user = UserFactory.create()
        plaid_item1 = PlaidItemFactory.create(user=user)
        plaid_item2 = PlaidItemFactory.create(user=user)
        plaid_items_ids_set = set([plaid_item1.id, plaid_item2.id])
        with logged_in_client(user) as client:
            resp = client.get("/plaid/items")
            assert resp.status_code == 200
            assert set(p["id"] for p in resp.json) == plaid_items_ids_set
