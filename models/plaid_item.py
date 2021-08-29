from datetime import datetime
from app import db
from common.database import db_session
from typing import Any, Dict, Optional


class PlaidItem(db.Model):  # type: ignore
    __tablename__ = "plaid_items"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    item_id = db.Column(db.String(255), nullable=False, index=True)
    access_token = db.Column(db.String(255), nullable=True)

    institution_id = db.Column(db.String(50), nullable=False)
    institution_name = db.Column(db.String(255))

    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), onupdate=datetime.utcnow)

    user = db.relationship("User", backref="plaid_items")
    plaid_accounts = db.relationship(
        "PlaidAccount",
        back_populates="plaid_item",
        order_by="PlaidAccount.id",
        cascade="all, delete-orphan",
        lazy="joined",
    )

    __table_args__ = (db.UniqueConstraint("user_id", "institution_id"),)

    @classmethod
    def create_plaid_item(
        cls,
        access_token: str,
        item_response: Dict[str, Any],
        institution_name: str,
        user_id: int,
    ) -> "PlaidItem":
        """
        Creates PlaidItem object
        :param access_token: Access token used in the Plaid API request
        :param item_response: Item response from Plaid API
        :param institution_name: Institution name from PlaidLink metadata
        :param user_id:
        :return: transient PlaidItem object
        """
        with db_session() as session:
            institution_id = item_response["institution_id"]
            plaid_item_id = item_response["item_id"]
            plaid_item = cls(
                user_id=user_id,
                institution_id=institution_id,
                institution_name=institution_name,
                item_id=plaid_item_id,
                access_token=access_token,
            )
            session.add(plaid_item)
            session.commit()
            return plaid_item

    @classmethod
    def get_plaid_item(cls, plaid_item_id: str) -> Optional["PlaidItem"]:
        with db_session() as session:
            item = (
                session.query(cls).filter(cls.item_id == plaid_item_id).one_or_none()
            )  # type: Optional[PlaidItem]
            return item

    def delete(self) -> None:
        with db_session() as session:
            session.delete(self)
            session.commit()
