# type: ignore
from models.plaid_account import PlaidAccount
from tests.mocks.plaid_response import accounts_response
from tests.factories import PlaidAccountFactory, PlaidItemFactory


class TestPlaidAccount:
    def test_get_plaid_account(self) -> None:
        plaid_account = PlaidAccountFactory.create()
        res = PlaidAccount.get_plaid_account(plaid_account.account_id)
        assert res == plaid_account

    def test_create_plaid_accounts(self) -> None:
        plaid_item = PlaidItemFactory.create()
        plaid_accounts = PlaidAccount.create_plaid_accounts(
            plaid_item=plaid_item, accounts=accounts_response["accounts"]
        )
        assert len(plaid_accounts) == 3

        account = accounts_response["accounts"][0]
        plaid_account = next(
            pa for pa in plaid_accounts if account["account_id"] == pa.account_id
        )
        assert plaid_account
        assert plaid_account.item_id == plaid_item.id
        assert plaid_account.mask == account["mask"]
        assert plaid_account.plaid_subtype == account["subtype"]
        assert plaid_account.plaid_type == account["type"]
        assert plaid_account.official_name == account["official_name"]
        assert plaid_account.name == account["name"]
        assert plaid_account.current_balance == account["balances"]["current"]
