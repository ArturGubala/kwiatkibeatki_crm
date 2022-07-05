from marshmallow import post_load
from flask_marshmallow import fields

from . import marshmallow
from .models import User


class UserSchema(marshmallow.Schema):
    name = fields.Str()
    surname = fields.Str()
    phone_number = fields.Str()
    email_address = fields.Email()

    @post_load
    def make_user(self, data, **kwargs) -> dict:
        return User(**data)
