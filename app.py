from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from schema import schema

from db import db
from route import ticket
import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/data/ticket.db'
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.json'
    swagger_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "CRUD app"
        }
    )
    app.register_blueprint(swagger_blueprint, url_prefix=SWAGGER_URL)
    app.register_blueprint(ticket.bp)

    with app.app_context():
        db.init_app(app)
        db.create_all()
        schema.init_app(app)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
