from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_manager
import json

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "dev_secret_key")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "main.login_page"

    from .modals import User, Tasks

    from .routes import main
    app.register_blueprint(main)

    @app.template_filter("from_json")
    def from_json_filter(value):
        try:
            return json.loads(value) if value else []
        except Exception:
            return []

    return app
