from common.exceptions import ValidationError
from app import config, logger
from plaid import Client
from typing import Any, Dict


client = Client(
    client_id=config.PLAID_CLIENT_ID,
    secret=config.PLAID_SECRET,
    public_key=config.PLAID_PUBLIC_KEY,
    environment=config.PLAID_ENV,
)


def get_access_token(public_token: str) -> str:
    """
    get access token from a public token
    """
    if not public_token:
        raise ValidationError("No public token was given")

    exchange_response = client.Item.public_token.exchange(public_token)
    logger.debug("public token: " + public_token)
    logger.debug("access token: " + exchange_response["access_token"])
    logger.debug("item ID: " + exchange_response["item_id"])
    access_token = exchange_response["access_token"]  # type: str
    return access_token


def get_plaid_accounts(access_token: str) -> Dict[Any, Any]:
    accounts = client.Accounts.get(access_token)  # type: Dict[Any, Any]
    return accounts
