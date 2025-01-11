from datetime import date

from . import db

#tabla resultante de conexion jugador-equipo
jugador_equipo = db.Table( 
    "jugador_equipo",
    db.Column("dni_jugador", db.Integer, db.ForeignKey('jugador.dni'), primary_key = True),
    db.Column("id_equipo", db.String(25), db.ForeignKey('equipo.id'), primary_key = True),
    db.Column("categoria", db.Enum('Sub-18', 'Sub-21' 'Mayores', name='categoria_enum', create_type=False), primary_key=True),
    
    db.Column("nro_camiseta", db.Integer,nullable=False),
    db.Column("posicion", db.String(10), nullable=False)
)

class Jugador(db.Model):
    __tablename__ = "jugador"

    dni = db.Column(db.Integer, primary_key=True)
    nya = db.Column(db.String(30), nullable=False)
    sexo = db.Column(db.Enum('M','F', name="sexo_enum", create_type=False), nullable=False)
    telefono = db.Column(db.String(15), nullable=True, default="0")
    fecha_nac = db.Column(db.Date, nullable=False)
    direccion = db.Column(db.String(35),nullable=True, default="")
    #Relacion uno a uno
    equipo_dirigido = db.relationship('Equipo', backref='jugador', uselist=False)
    # Relacion muchos a muchos
    equipos = db.relationship("Equipo", secondary="jugador_equipo",back_populates="jugadores")

    def __repr__(self):
        return f"{self.nya}"
    
    def ya_existe_en_la_bd(self):
        """ Revisa la base de datos en busca del jugador.
         Retornos:
         True, si el jugador existe en la bd/
         False, si el jugador no existe en la bd """
        return self.query.filter_by(dni=self.dni).scalar() != None

        
class Equipo(db.Model):
    __tablename__ = "equipo"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(25))
    contacto = db.Column(db.String(30),nullable=True, default="")
    division = db.Column(db.String(25), nullable=True, default="")
    fecha_ingreso = db.Column(db.Date,nullable=False)
    #Relacion uno a uno
    entrenador_id = db.Column(db.String(30), db.ForeignKey('jugador.dni'), nullable=True, unique=True) #clave foranea de jugador
    # Relacion muchos a muchos
    jugadores = db.relationship("Jugador",secondary="jugador_equipo",back_populates="equipos")
    
    def __repr__(self):
        return f"{self.nombre}"
    
    def ya_existe_en_la_bd(self):
        """ Revisa la base de datos en busca del equipo.
         Retornos:
         True, si el equipo existe en la bd/
         False, si el equipo no existe en la bd """
        return self.query.filter_by(nombre=self.nombre).scalar() != None
