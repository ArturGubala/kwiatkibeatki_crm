from flask import Flask
from flask_migrate import Migrate

from .config import Configuration
from .database import db

migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Configuration)

    db.init_app(app)

    migrate.init_app(app=app, db=db)

    return app
