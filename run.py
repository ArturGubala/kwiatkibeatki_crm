import os

import dotenv
from dotenv import load_dotenv

from app import create_app
from app.database import db

load_dotenv()


def create_db(app):

    with app.app_context():
        if not os.path.exists(os.getenv('RELATIVE_PATH_TO_DB')):
            db.create_all()


if __name__ == "__main__":
    app = create_app()
    create_db(app)
    app.run(host=os.getenv('HOST'), port=os.getenv('PORT'))
