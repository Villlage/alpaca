from models.plaid_item import PlaidItem
from tests.mocks.plaid_response import item_response
from tests.factories import UserFactory, PlaidItemFactory


class TestPlaidItem:
    def test_get_plaid_item(self) -> None:
        plaid_item = PlaidItemFactory.create()
        res = PlaidItem.get_plaid_item(plaid_item.item_id)
        assert res == plaid_item

    def test_delete(self) -> None:
        plaid_item = PlaidItemFactory.create()
        plaid_item_id = plaid_item.item_id
        plaid_item.delete()
        res = PlaidItem.get_plaid_item(plaid_item_id)
        assert res is None

    def test_save_plaid_item(self) -> None:
        user = UserFactory.create()
        access_token = "abc123"

        plaid_item = PlaidItem.create_plaid_item(
            access_token=access_token,
            item_response=item_response,
            user_id=user.id,
            institution_name="Citi",
        )
        assert plaid_item.user_id == user.id
        assert plaid_item.institution_id == item_response["institution_id"]
        assert plaid_item.item_id == item_response["item_id"]
        assert plaid_item.access_token == access_token

    def test_get_plaid_items_for_user(self) -> None:
        user1 = UserFactory.create()
        user2 = UserFactory.create()

        plaid_item1 = PlaidItemFactory.create(user=user1)
        plaid_item2 = PlaidItemFactory.create(user=user1)
        PlaidItemFactory.create(user=user2)

        plaid_items = user1.plaid_items
        assert len(plaid_items) == 2
        assert set([p.id for p in plaid_items]) == set([plaid_item1.id, plaid_item2.id])
