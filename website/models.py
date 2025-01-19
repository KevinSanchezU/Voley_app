from datetime import date

from . import db

#clase resultante de conexion jugador-equipo
class JugadorEquipo(db.Model):
    __tablename__ ="jugadorequipo"
    dni_jugador = db.Column("jugador.dni",db.Integer, db.ForeignKey("jugador.dni", ondelete="CASCADE"), primary_key=True)
    id_equipo = db.Column("equipo.id",db.Integer, db.ForeignKey("equipo.id", ondelete="CASCADE"), primary_key=True)
    categoria = db.Column(db.Enum('Sub-18', 'Sub-21', 'Mayores segunda', 'Mayores primera', name='categoria_enum', create_type=False),nullable=False)

    nro_camiseta = db.Column(db.Integer,nullable=False)
    posicion = db.Column(db.Enum('Punta', 'Central', 'Libero', 'Armador', 'Opuesto', name='posicion_enum', create_type=False))

    jugador = db.relationship("Jugador", back_populates="equipos")
    equipo = db.relationship("Equipo", back_populates="jugadores")

    def __repr__(self):
        return f"{self.dni_jugador}, {self.id_equipo}, {self.posicion}"
    
    def to_json(self):
        return {
            "dniJugador":self.dni_jugador,
            "idEquipo":self.id_equipo,
            "categoria":self.categoria,
            "nroCamiseta":self.nro_camiseta,
            "posicion":self.posicion
        }

class Jugador(db.Model):
    __tablename__ = "jugador"

    dni = db.Column(db.Integer, primary_key=True)
    nya = db.Column(db.String(45), nullable=False)
    sexo = db.Column(db.Enum('M','F', name="sexo_enum", create_type=False), nullable=False)
    telefono = db.Column(db.String(15), nullable=True, default=None)
    fecha_nac = db.Column(db.Date, nullable=False)
    direccion = db.Column(db.String(75),nullable=True, default=None)
    #Relacion uno a uno
    equipo_dirigido = db.relationship('Equipo', backref='jugador', uselist=False)
    # Relacion muchos a muchos
    equipos = db.relationship("JugadorEquipo",back_populates="jugador", cascade="all, delete-orphan")

    def __repr__(self):
        return f"{self.nya}"
    
    def to_json(self):
        return {
            "dni":self.dni,
            "nya":self.nya,
            "sexo":self.sexo,
            "telefono":self.telefono,
            "fechaNac":self.fecha_nac,
            "direccion":self.direccion,
            "equipoDirigido": self.equipo_dirigido,
            "equipos": [equipo.equipo.nombre for equipo in self.equipos]
        }

        
class Equipo(db.Model):
    __tablename__ = "equipo"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(45))
    contacto = db.Column(db.String(60),nullable=True, default=None)
    division = db.Column(db.Enum('M','F', name="division_enum", create_type=False), nullable=False)
    fecha_ingreso = db.Column(db.Date,nullable=False)
    #Relacion uno a uno
    entrenador_id = db.Column(db.Integer, db.ForeignKey('jugador.dni', ondelete="SET NULL"), nullable=True, unique=True) #clave foranea de jugador
    # Relacion muchos a muchos
    jugadores = db.relationship("JugadorEquipo", back_populates="equipo", cascade="all, delete-orphan")
    
    __table_args__ = (db.UniqueConstraint("nombre","division", name="unique_nombre_division"),)

    def __repr__(self):
        return f"{self.nombre}"
    
    def to_json(self):
        return {
            "id":self.id,
            "nombre":self.nombre,
            "contacto":self.contacto,
            "division":self.division,
            "fechaIngreso":self.fecha_ingreso,
            "entrenadorId":self.entrenador_id,
            "jugadores": [jugador.jugador.nya for jugador in self.jugadores]
        }
