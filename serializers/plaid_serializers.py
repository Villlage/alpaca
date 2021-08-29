from marshmallow import Schema, fields

from app import ma
from models.plaid_item import PlaidItem


class PlaidRequestSchema(Schema):  # type: ignore
    public_token = fields.String(required=True, allow_none=False)
    metadata = fields.Dict(required=True, allow_none=False)


class PlaidItemSchema(ma.ModelSchema):  # type: ignore
    class Meta:
        model = PlaidItem
        include_fk = True
        exclude = ("access_token", "item_id", "user")

    public_token = fields.String(required=False)


plaid_request_schema = PlaidRequestSchema()
plaid_item_schema = PlaidItemSchema()
