import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from uuid import UUID

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.secret_key = os.environ.get('SECRET_KEY', 'dev')

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.signin'

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return User.query.get(UUID(user_id))
        except ValueError:
            return None
    
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app