from flask import Flask
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

from .config import Configuration
from .database import db

migrate = Migrate()
marshmallow = Marshmallow()
login_manager = LoginManager()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Configuration)

    db.init_app(app)

    migrate.init_app(app=app, db=db)
    login_manager.init_app(app)

    from .views import (
        LoginView,
        LogoutView,
        DashboardView,
        CatalogueView,
        ProfileView,
        DocumentView
    )

    app.add_url_rule("/", view_func=LoginView.as_view("login_view"))
    app.add_url_rule("/logout", view_func=LogoutView.as_view("logout_view"))
    app.add_url_rule("/dashboard",
                     view_func=DashboardView.as_view("dashboard_view"))
    app.add_url_rule("/catalogue",
                     view_func=CatalogueView.as_view("catalogue_view"))
    app.add_url_rule("/profile",
                     view_func=ProfileView.as_view("profile_view"))
    app.add_url_rule("/dokument",
                     view_func=DocumentView.as_view("document_view"))

    return app
