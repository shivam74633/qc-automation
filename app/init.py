from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    from app.tasks.views import tasks_blueprint
    app.register_blueprint(tasks_blueprint, url_prefix='/tasks')

    from app.users.views import users_blueprint
    app.register_blueprint(users_blueprint, url_prefix='/users')

    return app
