from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config 

from flask_bcrypt import Bcrypt

from flask_jwt_extended import JWTManager

from flask_cors import CORS 

db=SQLAlchemy()
migrate=Migrate()
bcrypt= Bcrypt()
jwt=JWTManager()

def create_app():#Sets up and configures the Flask app.
    app=Flask(__name__)
    app.config.from_object(Config)  # Load config from the Config class
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app,db)
    from .models import User,Book,Loan
    CORS(app) #Enables cross-origin requests from any domain.

    #import blue prints 
    from .library_utils import library_blueprint
    #register blue prints 
    app.register_blueprint(library_blueprint)
    return app