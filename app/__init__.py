from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config

from flask_bcrypt import Bcrypt

from flask_jwt_extended import JWTManager

from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    from .models import User, Book, Loan

<<<<<<< HEAD
    #import blue prints 
    from .library_utils import library_blueprint
    #register blue prints 
    app.register_blueprint(library_blueprint)
    return app
=======
    CORS(app)
    from .routes import loan

    app.register_blueprint(loan)
    migrate.init_app(app, db)
    from .models import User, Book, Loan

    CORS(app)  # Enables cross-origin requests from any domain.

    # import blue prints
    from .endpoints import book_blueprint

    # register blue prints
    app.register_blueprint(book_blueprint)
    # ... more blueprints here.

    # import blue prints
    # import blue prints
    from .auth import auth_blueprint

    # register blue prints
    app.register_blueprint(auth_blueprint)
    return app
>>>>>>> main
