from datetime import datetime
from sqlalchemy import ForeignKey

from .database import db


class Role(db.Model):
    __tablename__ = "role"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=50), nullable=False, unique=True)

    user = db.relationship("User", backref="role", uselist=False)

    def __init__(self, name: str) -> None:
        self.name = name


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, ForeignKey("role.id"), nullable=False)
    name = db.Column(db.String(length=50), nullable=False, unique=True)
    surname = db.Column(db.String(length=50))
    phone_number = db.Column(db.String(length=15))
    email_address = db.Column(db.String(length=50), nullable=False,
                              unique=True)

    document = db.relationship("Document", backref="user", uselist=False)

    def __init__(self, role_id: int, name: str, surname: str, phone_number: str, email_address: str) -> None:
        self.role_id = role_id
        self.name = name
        self.surname = surname
        self.phone_number = phone_number
        self.email_address = email_address


class CatalogueType(db.Model):
    __tablename__ = "catalogue_type"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=50), nullable=False, unique=True)

    catalogue = db.relationship("Catalogue", backref="catalogue_type",
                                uselist=False)

    def __init__(self, name: str):
        self.name = name


class Producer(db.Model):
    __tablename__ = "producer"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=50), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False)
    phone_number = db.Column(db.String(length=50))

    catalogue = db.relationship("Catalogue", backref="producer", uselist=False)

    def __init__(self, name: str, email_address: str, phone_number: str) -> None:
        self.name = name
        self.email_address = email_address
        self.phone_number = phone_number


class BulkPackType(db.Model):
    __tablename__ = "bulk_pack_type"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=50), nullable=False, unique=True)
    abbreviation = db.Column(db.String(length=10), nullable=False, unique=True)

    catalogue = db.relationship("Catalogue", backref="bulk_pack_type",
                                uselist=False)

    def __init__(self, name: str, abbreviation: str) -> None:
        self.name = name
        self.abbreviation = abbreviation


class MeasurementUnit(db.Model):
    __tablename__ = "measurement_unit"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=50), nullable=False, unique=True)
    abbreviation = db.Column(db.String(length=5), nullable=False, unique=True)

    catalogue = db.relationship("Catalogue", backref="measurement_unit",
                                uselist=False)

    def __init__(self, name: str, abbreviation: str) -> None:
        self.name = name
        self.abbreviation = abbreviation


class Catalogue(db.Model):
    __tablename__ = "catalogue"

    id = db.Column(db.Integer, primary_key=True)
    measurement_unit_id = db.Column(db.Integer, ForeignKey("measurement_unit.id"),
                                    nullable=False)
    catalogue_type_id = db.Column(db.Integer, ForeignKey("catalogue_type.id"),
                                  nullable=False)
    bulk_pack_id = db.Column(db.Integer, ForeignKey("bulk_pack_type.id"),
                             nullable=False)
    producer_id = db.Column(db.Integer, ForeignKey("producer.id"),
                            nullable=False)
    stock_code = db.Column(db.String(length=50), nullable=False, unique=True)
    name = db.Column(db.String(length=200), unique=True)
    alias = db.Column(db.String(length=50), unique=True)
    last_purchase_price = db.Column(db.Numeric(18, 2))
    bulk_pack_capacity = db.Column(db.Numeric(18, 2))
    no_bulk_pack_on_palette = db.Column(db.Numeric(18, 2))
    burning_time = db.Column(db.Numeric(18, 2))
    height = db.Column(db.Numeric(18, 2))
    width = db.Column(db.Numeric(18, 2))
    diameter = db.Column(db.Numeric(18, 2))

    def __init__(self, measurement_unit_id: int, catalogue_type_id: int, bulk_pack_id: int,
                 producer_id: int, stock_code: str, name: str, alias: str, last_purchase_price: float,
                 bulk_pack_capacity: float, burning_time: float, height: float, width: float,
                 diameter: float) -> None:
        self.measurement_unit_id = measurement_unit_id
        self.catalogue_type_id = catalogue_type_id
        self.bulk_pack_id = bulk_pack_id
        self.producer_id = producer_id
        self.stock_code = stock_code
        self.name = name
        self.alias = alias
        self.last_purchase_price = last_purchase_price
        self.bulk_pack_capacity = bulk_pack_capacity
        self.burning_time = burning_time
        self.height = height
        self.width = width
        self.diameter = diameter


class Warehouse(db.Model):
    __tablename__ = "warehouse"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=100), nullable=False, unique=True)
    code = db.Column(db.String(length=10), nullable=False, unique=True)

    document = db.relationship("Document", backref="warehouse", uselist=False)

    def __init__(self, name: str, code: str) -> None:
        self.name = name
        self.code = code


class DocumentType(db.Model):
    __tablename__ = "document_type"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=50), nullable=False, unique=True)
    abbreviation = db.Column(db.String(length=10), nullable=False, unique=True)
    numeration_template = db.Column(db.String(length=50), nullable=False)

    document = db.relationship("Document", backref="document_type",
                               uselist=False)

    def __init__(self, name: str, abbreviation: str, numeration_template: str) -> None:
        self.name = name
        self.abbreviation = abbreviation
        self.numeration_template = numeration_template


class Document(db.Model):
    __tablename__ = "document"

    id = db.Column(db.Integer, primary_key=True)
    document_type_id = db.Column(db.Integer, ForeignKey("document_type.id"),
                                 nullable=False)
    user_id = db.Column(db.Integer, ForeignKey("user.id"), nullable=False)
    warehouse_id = db.Column(db.Integer, ForeignKey("warehouse.id"),
                             nullable=False)
    number = db.Column(db.String(length=50), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, nullable=False)
    modification_date = db.Column(db.DateTime, nullable=False)
    total = db.Column(db.String(length=50), nullable=False)

    def __init__(self, document_type_id: int, user_id: int, warehouse_id: int, number: str,
                 date_added: datetime, modification_date: datetime, total: float) -> None:
        self.document_type_id = document_type_id
        self.user_id = user_id
        self.warehouse_id = warehouse_id
        self.number = number
        self.date_added = date_added
        self.modification_date = modification_date
        self.total = total


class Item(db.Model):
    __tablename__ = "item"

    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, ForeignKey("document_type.id"),
                            nullable=False)
    catalogue_id = db.Column(db.Integer, ForeignKey("catalogue.id"),
                             nullable=False)
    quantity = db.Column(db.Numeric(18, 2), nullable=False)
    price = db.Column(db.Numeric(18, 2), nullable=False)
    amount = db.Column(db.Numeric(18, 2), nullable=False)

    def __init__(self, document_id: int, catalogue_id: int, quantity: float, price: float,
                 amount: float) -> None:
        self.document_id = document_id
        self.catalogue_id = catalogue_id
        self.quantity = quantity
        self.price = price
        self.amount = amount
