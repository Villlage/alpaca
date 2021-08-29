from typing import Dict, Any, List
from third_party.plaid.plaid_client import (
    get_access_token,
    get_plaid_accounts,
    get_plaid_accounts,
)
from models.plaid_item import PlaidItem
from models.plaid_account import PlaidAccount
from models.user import User


def create_plaid_item(
    user: User, public_token: str, metadata: Dict[Any, Any]
) -> PlaidItem:
    access_token = get_access_token(public_token)

    accounts_response = get_plaid_accounts(access_token)

    plaid_item = save_plaid_item_and_accounts(
        access_token=access_token,
        user_id=user.id,
        institution_name=metadata["institution"]["name"],
        accounts_response=accounts_response,
    )
    return plaid_item


def save_plaid_item_and_accounts(
    access_token: str,
    user_id: int,
    institution_name: str,
    accounts_response: Dict[Any, Any],
) -> PlaidItem:
    """
    save a plaid item and its accounts
    :param access_token: access token from plaid 
    :param user_id: The user associated with it
    :param institution_name: Institution name from PlaidLink metadata
    :param accounts_response: accounts response from Plaid
    :returns: the plaid item that was created 
    """

    plaid_item = PlaidItem.create_plaid_item(
        access_token, accounts_response["item"], institution_name, user_id,
    )
    accounts = accounts_response["accounts"]  # type: List[Dict[Any, Any]]
    PlaidAccount.create_plaid_accounts(plaid_item, accounts)

    return plaid_item
