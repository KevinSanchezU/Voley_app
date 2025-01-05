from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from website import crear_app
from website.models import db, Jugador, Equipo, jugador_equipo

app = crear_app()

#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///voley_app_database.db"

#db.init_app(app)

if __name__ == "__main__":
    app.run(debug=True)