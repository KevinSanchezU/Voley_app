from datetime import date

from . import db

#clase resultante de conexion jugador-equipo
class JugadorEquipo(db.Model):
    __tablename__ ="jugadorequipo"
    dni_jugador = db.Column("jugador.dni",db.Integer, db.ForeignKey("jugador.dni", ondelete="CASCADE"), primary_key=True)
    id_equipo = db.Column("equipo.id",db.Integer, db.ForeignKey("equipo.id", ondelete="CASCADE"), primary_key=True)
    categoria = db.Column(db.Enum('Sub-18', 'Sub-21', 'Mayores segunda', 'Mayores primera', name='categoria_enum', create_type=False),nullable=False)

    nro_camiseta = db.Column(db.Integer,nullable=False)
    posicion = db.Column(db.Enum('Punta', 'Central' 'Libero', 'Armador', 'Opuesto', name='posicion_enum', create_type=False))

    jugador = db.relationship("Jugador", back_populates="equipos")
    equipo = db.relationship("Equipo", back_populates="jugadores")


class Jugador(db.Model):
    __tablename__ = "jugador"

    dni = db.Column(db.Integer, primary_key=True)
    nya = db.Column(db.String(45), nullable=False)
    sexo = db.Column(db.Enum('M','F', name="sexo_enum", create_type=False), nullable=False)
    telefono = db.Column(db.String(15), nullable=True, default="0")
    fecha_nac = db.Column(db.Date, nullable=False)
    direccion = db.Column(db.String(75),nullable=True, default="")
    #Relacion uno a uno
    equipo_dirigido = db.relationship('Equipo', backref='jugador', uselist=False)
    # Relacion muchos a muchos
    equipos = db.relationship("JugadorEquipo",back_populates="jugador", cascade="all, delete-orphan")

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
    nombre = db.Column(db.String(45))
    contacto = db.Column(db.String(60),nullable=True, default="")
    division = db.Column(db.Enum('M','F', name="division_enum", create_type=False), nullable=False)
    fecha_ingreso = db.Column(db.Date,nullable=False)
    #Relacion uno a uno
    entrenador_id = db.Column(db.Integer, db.ForeignKey('jugador.dni', ondelete="SET NULL"), nullable=True, unique=True) #clave foranea de jugador
    # Relacion muchos a muchos
    jugadores = db.relationship("JugadorEquipo", back_populates="equipo", cascade="all, delete-orphan")
    
    __table_args__ = (db.UniqueConstraint("nombre","division", name="unique_nombre_division"),)

    def __repr__(self):
        return f"{self.nombre}"
    
    def ya_existe_en_la_bd(self): #except IntegrityError as e:
        """ Revisa la base de datos en busca del equipo.
         Retornos:
         True, si el equipo existe en la bd/
         False, si el equipo no existe en la bd """
        return self.query.filter_by(nombre=self.nombre).scalar() != None
