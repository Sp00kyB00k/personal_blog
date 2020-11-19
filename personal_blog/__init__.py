from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from personal_blog.config import Config


db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from .users import users as user_blueprint
    app.register_blueprint(user_blueprint)

    from .posts import posts as post_blueprint
    app.register_blueprint(post_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .errors import errors as error_blueprint
    app.register_blueprint(error_blueprint)

    return app
