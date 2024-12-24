from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///voley_app_database.db"
db = SQLAlchemy(app)

class Jugador(db.Model):
    dni = db.Column(db.Integer, primary_key=True)
    categoria = db.Column(db.String(20), primary_key=True)
    nya = db.Column(db.String(30), nullable=False)
    telefono = db.Column(db.Integer, nullable=True, default="0")
    fecha_nac = db.Column(db.Datetime, nullable=False)
    direccion = db.Column(db.String(35),nullable=True)
    
    
@app.route("/")
def home():
    return "<h1>Hello, World!</h1>"

if __name__ == "__main__":
    app.run(debug=True)