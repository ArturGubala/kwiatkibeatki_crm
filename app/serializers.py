from flask_marshmallow.fields import fields

from . import marshmallow
from .models import (
    AppUser, Producer, BulkPackType, Catalogue,
    DocumentType, Document, Item
)


class UserSchema(marshmallow.Schema):
    name = fields.Str()
    surname = fields.Str()
    phone_number = fields.Str()
    email_address = fields.Email()

    @marshmallow.post_load
    def make_user(self, data, **kwargs) -> dict:
        return AppUser(**data)


class ProducerSchema(marshmallow.Schema):
    name = fields.Str()
    email_address = fields.Email()
    phone_number = fields.Str()

    @marshmallow.post_load
    def make_producer(self, data, **kwargs) -> dict:
        return Producer(**data)


class BulkPackTypeSchema(marshmallow.Schema):
    name = fields.Str()
    abbreviation = fields.Str()

    @marshmallow.post_load
    def make_bulk_pack_type(self, data, **kwargs) -> dict:
        return BulkPackType(**data)


class CatalogueSchema(marshmallow.Schema):
    measurement_unit_id = fields.Int()
    catalogue_type_id = fields.Int()
    bulk_pack_id = fields.Int()
    producer_id = fields.Int()
    stack_code = fields.Str()
    name = fields.Str()
    alias = fields.Str()
    last_purchase_price = fields.Decimal()
    bulk_pack_capacity = fields.Float()
    no_bulk_pack_on_palette = fields.Int()
    burning_time = fields.Float()
    height = fields.Float()
    width = fields.Float
    diameter = fields.Float

    @marshmallow.post_load
    def make_catalogue(self, data, **kwargs) -> dict:
        return Catalogue(**data)


class DocumentTypeSchema(marshmallow.Schema):
    name = fields.Str()
    abbreviation = fields.Str()
    numeration_template = fields.Str()

    @marshmallow.post_load
    def make_document_type(self, data, **kwargs) -> dict:
        return DocumentType(**data)


class DocumentSchema(marshmallow.Schema):
    document_type_id = fields.Int()
    user_id = fields.Int()
    warehouse_id = fields.Int()
    number = fields.Str()
    total = fields.Decimal()

    @marshmallow.post_load
    def make_document(self, data, **kwargs) -> dict:
        return Document(**data)


class ItemSchema(marshmallow.Schema):
    document_id = fields.Int()
    catalogue_id = fields.Int()
    quantity = fields.Float()
    price = fields.Decimal()
    price = fields.Float()

    @marshmallow.post_load
    def make_item(self, data, **kwargs) -> dict:
        return Item(**data)
