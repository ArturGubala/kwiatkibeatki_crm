from flask import Flask
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

from .config import Configuration
from .database import db

migrate = Migrate()
marshmallow = Marshmallow()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Configuration)

    db.init_app(app)

    migrate.init_app(app=app, db=db)

    return app
