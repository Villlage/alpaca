from marshmallow import Schema, fields

# from marshmallow.validate import OneOf, Range
# from app import ma


class LoginSchema(Schema):  # type: ignore
    email = fields.Email(allow_none=False, required=True)
    password = fields.Str(allow_none=False, required=True)


login_schema = LoginSchema()
