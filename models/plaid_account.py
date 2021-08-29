from app import db
from common.database import db_session
from typing import Any, Dict, List, Optional
from models.plaid_item import PlaidItem


class PlaidAccount(db.Model):  # type: ignore
    __tablename__ = "plaid_accounts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    item_id = db.Column(
        db.Integer, db.ForeignKey("plaid_items.id"), index=True, nullable=False
    )
    plaid_item = db.relationship("PlaidItem", back_populates="plaid_accounts")

    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), index=True, nullable=False
    )

    account_id = db.Column(db.String(255), nullable=False, index=True)
    plaid_type = db.Column(db.String(255), nullable=False)
    plaid_subtype = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    official_name = db.Column(db.String(255))

    current_balance = db.Column(db.Float, nullable=False)
    mask = db.Column(db.String(4), nullable=True)

    user = db.relationship("User", backref="plaid_account")

    @classmethod
    def get_plaid_account(cls, account_id: str) -> Optional["PlaidAccount"]:
        with db_session() as session:
            account = (
                session.query(cls).filter(cls.account_id == account_id).one_or_none()
            )  # type: Optional[PlaidAccount]
            return account

    @classmethod
    def create_plaid_accounts(
        cls, plaid_item: "PlaidItem", accounts: List[Dict[Any, Any]]
    ) -> List["PlaidAccount"]:
        """
        Creates PlaidAccount objects
        :param plaid_item: PlaidItem object
        :param accounts: Accounts response from Plaid API
        :return: List of transient PlaidAccount objects
        """
        plaid_accounts = []
        with db_session() as session:
            for account in accounts:
                balance = _get_balance(account)
                plaid_account = cls(
                    item_id=plaid_item.id,
                    user_id=plaid_item.user_id,
                    name=account["name"],
                    official_name=account["official_name"],
                    account_id=account["account_id"],
                    plaid_type=account["type"],
                    plaid_subtype=account["subtype"],
                    current_balance=balance,
                    mask=account["mask"],
                )

                plaid_accounts.append(plaid_account)

            session.add_all(plaid_accounts)
            session.commit()

        return plaid_accounts


def _get_balance(account: Dict[Any, Any]) -> float:
    balance = account["balances"].get("current")
    if balance is None:
        balance = account["balances"]["available"]
    return balance  # type: ignore
