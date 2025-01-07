from flask import Blueprint, request, render_template
from .models import Equipo, Jugador
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
            db.session.add(nuevo_equipo)
            db.session.commit()
            return "POST REQUEST"
        else:
            return "ERROR EN LOS PARAMETROS"

@views.route("/jugadores")
def jugadores():
    #funcion que muestra todos los jugadores
    #Jugador.query.all()
    return "<h1>Todos los jugadores!</h1>"