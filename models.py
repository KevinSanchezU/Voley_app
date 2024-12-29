from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Jugador(db.Model):
    __table__ = "jugador"

    dni = db.Column(db.Integer, primary_key=True)
    nya = db.Column(db.String(30), nullable=False)
    telefono = db.Column(db.Integer, nullable=True, default="0")
    fecha_nac = db.Column(db.Datetime, nullable=False)
    direccion = db.Column(db.String(35),nullable=True)
    #Relacion uno a uno
    equipo_dirigido = db.relationship('Equipo', backref='jugador')
    # Relacion muchos a muchos
    equipo = db.relationship("Equipo", secondary = "jugador_equipo",back_populates="jugador")

class Equipo(db.Model):
    __table__ = "equipo"

    nombre = db.Column(db.String(25), primary_key=True)
    contacto = db.Column(db.String(30),nullable=True)
    division = db.Column(db.String(25), nullable=True)
    fecha_ingreso = db.Column(db.Datetime,nullable=False)
    #Relacion uno a uno
    entrenador_id = db.Column(db.String(30), db.ForeignKey('jugador.dni'), nullable=True) #clave foranea de jugador
    # Relacion muchos a muchos
    jugador = db.relationship("Jugador",secondary="jugador_equipo",back_populates="equipo")

jugador_equipo = db.Table( #tabla resultante de jugador JOIN equipo
    "jugador_equipo",
    db.Column("jugador_dni", db.Integer, db.ForeignKey('jugador.dni'), primary_key = True),
    db.Column("equipo_nombre", db.String(25), db.ForeignKey('equipo.nombre'), primary_key = True),
    db.Column("categoria", db.String(10), primary_key=True),
    
    db.Column("nro_camiseta", db.Integer,nullable=False),
    db.Column("posicion", db.String(10), nullable=False)
)