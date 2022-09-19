from flask import Flask

from .config import Configuration


def create_app():
    app = Flask(__name__)
    app.config.from_object(Configuration)

    from .views import (
        GetStatusView
    )

    app.add_url_rule("/status/<int:id>",
                     view_func=GetStatusView.as_view("status_view"))

    return app
