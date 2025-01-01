from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

#tabla resultante de jugador JOIN equipo
jugador_equipo = db.Table( 
    "jugador_equipo",
    db.Column("dni", db.Integer, db.ForeignKey('jugador.dni'), primary_key = True),
    db.Column("nombre", db.String(25), db.ForeignKey('equipo.nombre'), primary_key = True),
    db.Column("categoria", db.Enum('Sub-18', 'Sub-21' 'Mayores', name='categoria_enum', create_type=False), primary_key=True),
    
    db.Column("nro_camiseta", db.Integer,nullable=False),
    db.Column("posicion", db.String(10), nullable=False)
)

class Jugador(db.Model):
    __tablename__ = "jugador"

    dni = db.Column(db.Integer, primary_key=True)
    nya = db.Column(db.String(30), nullable=False)
    telefono = db.Column(db.String(15), nullable=True, default="0")
    fecha_nac = db.Column(db.Date, nullable=False)
    direccion = db.Column(db.String(35),nullable=True)
    #Relacion uno a uno
    equipo_dirigido = db.relationship('Equipo', backref='jugador', uselist=False)
    # Relacion muchos a muchos
    equipos = db.relationship("Equipo", secondary="jugador_equipo",back_populates="jugadores")

class Equipo(db.Model):
    __tablename__ = "equipo"

    nombre = db.Column(db.String(25), primary_key=True)
    contacto = db.Column(db.String(30),nullable=True)
    division = db.Column(db.String(25), nullable=True)
    fecha_ingreso = db.Column(db.Date,nullable=False)
    #Relacion uno a uno
    entrenador_id = db.Column(db.String(30), db.ForeignKey('jugador.dni'), nullable=True, unique=True) #clave foranea de jugador
    # Relacion muchos a muchos
    jugadores = db.relationship("Jugador",secondary="jugador_equipo",back_populates="equipos")

