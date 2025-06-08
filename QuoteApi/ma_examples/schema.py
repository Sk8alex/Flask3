from marshmallow import Schema, fields


class AuthorSchema(Schema):
    id = fields.Integer()
    name = fields.String(
        required=True, # обязательный параметр
        error_messages={"required": "field 'name' is required"}
        )
    email = fields.Email(
        required=True, # обязательный параметр
        error_messages={"required": "field 'email' is required"}
        )
    surname = fields.String()