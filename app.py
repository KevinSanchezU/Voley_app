from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db, Jugador, Equipo, jugador_equipo

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///voley_app_database.db"

db.init_app(app)


@app.route("/")
def home():
    return "<h1>Hello, World!</h1>"

if __name__ == "__main__":
    app.run(debug=True)