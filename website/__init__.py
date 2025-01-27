from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import path

db = SQLAlchemy()
DB_NAME = "voley_app_database.db"

def crear_app():
    app = Flask(__name__)
    CORS(app)
    
    app.config["SECRET_KEY"] = "this is a secret key, pero en espaniol"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    db.init_app(app)

    from .views import views

    app.register_blueprint(views,url_prefix="/api")
    
    from .models import Equipo,Jugador,JugadorEquipo

    crear_db(app)

    return app

def crear_db(app):
    with app.app_context():
        db.create_all()