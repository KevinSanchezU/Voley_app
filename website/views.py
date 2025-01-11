from flask import Blueprint, request, render_template
from .models import Equipo, Jugador, jugador_equipo
from datetime import date
from . import db


views = Blueprint("views", __name__)

def validar_division_equipo(division):
    if division not in ["Sub-18", "Sub-21", "Mayores", ""]:
        return False
    return True

def validar_nombre(nombre):
    if len(nombre) < 2:
        return False
    return True
def validar_fecha(fecha):
    # TO DO
    # No permitir fechas posteriores al dia actual
    return True
    
def validar_jugador(jugador):
    if len(jugador.dni) < 7:
        return False
    #Validar telefono?
    return True

@views.route("/")
def home():
    return "<h1> Bienvenido a la liga, elija si ver equipos o Jugadores</h1>"
@views.route("/equipos", methods=["GET","POST"])
def equipos():
    #funcion que muestra todos los equipos
    if request.method == "GET":
        equipos = Equipo.query.order_by(Equipo.nombre).all()
        if len(equipos) > 0:
            for equipo in equipos:
                print(f"Id del equipo: {equipo.id}")
                print(f"Nombre de equipo: {equipo.nombre}")
                print(f"Fecha de ingreso: {equipo.fecha_ingreso}")
                print(f"DNI de entrenador: {equipo.entrenador_id}")
                # A pesar de agregar un entrenador, este no aparece => entrenador_id es una clave foranea
        else:
            print("No hay equipos")
        return "<h1>Todos los equipos!</h1>"
    elif request.method == "POST":
        #Levantar valores del front
        nombre = request.form.get("nombre")
        contacto = request.form.get("contacto")
        division = request.form.get("division")
        fecha_ingreso = date.fromisoformat(request.form.get("fecha_ingreso")) #convertir string en un objeto date
        entrenador_id = request.form.get("entrenador")

        #Validar valores
        if validar_division_equipo(division) and validar_nombre(nombre) and validar_fecha(fecha_ingreso):
            #agregar equipo a la bd
            nuevo_equipo = Equipo(nombre=nombre, fecha_ingreso=fecha_ingreso,contacto=contacto, division=division,entrenador_id=entrenador_id)
            if nuevo_equipo.ya_existe_en_la_bd() == True:
                return "Equipo ya existe en la base de datos"
            db.session.add(nuevo_equipo)
            db.session.commit()
            return "Equipo agregado"
        else:
            return "ERROR EN LOS PARAMETROS"
    else:
        return "Eliminando equipo"

@views.route("/jugadores", methods=["GET","POST","PUT"])
def jugadores():
    if request.method == "GET":
        jugadores = Jugador.query.order_by(Jugador.dni).all()
        if len(jugadores) > 0:
            for jugador in jugadores:
                print(f"Nombre del jugador: {jugador.nya}")
                print(f"DNI del jugador: {jugador.dni}")
                print(f"Fecha de nacimiento: {jugador.fecha_nac}")
                print(f"Juega en: {jugador.equipos}")
                print(f"Entrenador en: {jugador.equipo_dirigido}")

        else:
            print("No hay jugadores")
        return "<h1>Todos los jugadores!</h1>"

    elif request.method == "POST":
        #Levantando info del jugador del front
        dni = request.form.get("dni")
        nya = request.form.get("nya")
        telefono = request.form.get("telefono")
        fecha_nac = date.fromisoformat(request.form.get("fecha_nac"))
        direccion = request.form.get("direccion")
        #creacion de jugador
        nuevo_jugador = Jugador(dni=dni,nya=nya,telefono=telefono,fecha_nac=fecha_nac,direccion=direccion)
        #Ver si hay un jugador con ese dni
        
        if nuevo_jugador.ya_existe_en_la_bd() == True:
            return "Jugador ya existe en la base de datos"
        #Agregar jugador a la bd
        db.session.add(nuevo_jugador)
        db.session.commit()

        return "Jugador agregado"

    else: #method PUT, agregando equipos dirigidos y a que equipo pertenece
        dni = request.form.get("dni")
        equipo_dirigido_form = request.form.get("equipo_dirigido")
        equipo_donde_juega_form = request.form.get("equipo")
        jugador = Jugador.query.filter_by(dni=dni).first()
        
        #consiguiendo el equipo dirigido
        equipo_dirigido = Equipo.query.get(equipo_dirigido_form)
        #consiguiendo el equipo donde juega
        equipo = Equipo.query.get(equipo_donde_juega_form)
        
        if equipo_dirigido.nombre == equipo.nombre:
            print("No podes dirigir y jugar en el mismo equipo")
        if equipo_dirigido is not None:
            jugador.equipo_dirigido = equipo_dirigido
        if equipo is not None:
            jugador.equipos.append(equipo)
        #db.session.commit()

        return "Metodo PUT"
    #Jugador.query.all()
""" Para llenar los atributos relationship en Models es necesario
asignarles un objeto del tipo especificado en la relacion """