from flask import Blueprint, request, render_template, jsonify
from sqlalchemy import exc
from .models import Equipo, Jugador, JugadorEquipo
from datetime import date
from . import db


views = Blueprint("views", __name__)

def validar_division_equipo(division):
    if division not in ["M","F"]:
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
@views.route("/equipos", methods=["GET","POST", "PUT"])
def equipos():
    #funcion que muestra todos los equipos
    if request.method == "GET":
        equipos = Equipo.query.order_by(Equipo.nombre).all()
        if len(equipos) > 0:
            for equipo in equipos:
                print(f"Id del equipo: {equipo.id}")
                print(f"Nombre de equipo: {equipo.nombre}")
                print(f"Fecha de ingreso: {equipo.fecha_ingreso}")
                print(f"Division: {equipo.division}")
                print(f"DNI de entrenador: {equipo.entrenador_id}")
                print(f"jugadores: {equipo.jugadores}")
        else:
            return jsonify({"Mensaje":"No hay equipos"})
        ## REVISANDO LA CLASE JUGADOREQUIPO
        jugador_equipo = JugadorEquipo.query.order_by(JugadorEquipo.id_equipo).all()
        if len(jugador_equipo) > 0:
            for asociacion in jugador_equipo:
                print(asociacion)
        else:
            print("No nay asociacion")

        return jsonify({"Mensaje":"201"})
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
            if entrenador_id is not None:
                print("buscando entrenador en la bd")
            nuevo_equipo = Equipo(nombre=nombre, fecha_ingreso=fecha_ingreso,contacto=contacto, division=division,entrenador_id=entrenador_id)
            try:
                db.session.add(nuevo_equipo)
                db.session.commit()
            except exc.IntegrityError as e:
                db.session.rollback()
                return f"Error: {e}"
            return jsonify({"Mensaje": f"Agregado {nombre} correctamente"})
        else:
            return "ERROR EN LOS PARAMETROS"
    else: # metodo PUT
        nombre = request.form.get("nombre")
        dni = request.form.get("dni")
        division = request.form.get("division")
        jugador = Jugador.query.filter_by(dni=dni).first()
        equipo = Equipo.query.filter_by(nombre=nombre,division=division).first()
        asociacion = JugadorEquipo(dni_jugador=jugador.dni, id_equipo=equipo.id,categoria="Mayores segunda", nro_camiseta=12,posicion="Opuesto")
        print(equipo.jugadores)
        db.session.add(asociacion)
        print(equipo.jugadores)
        try:
            db.session.commit()
        except exc.IntegrityError as e:
            return f"{e}"
        return jsonify({"mensaje":"Equipo cambiado con exito"})

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
        sexo = request.form.get("sexo")
        telefono = request.form.get("telefono")
        fecha_nac = date.fromisoformat(request.form.get("fecha_nac"))
        direccion = request.form.get("direccion")
        #creacion de jugador
        nuevo_jugador = Jugador(dni=dni,nya=nya,sexo=sexo,telefono=telefono,fecha_nac=fecha_nac,direccion=direccion)
        
        try:
            db.session.add(nuevo_jugador)
            db.session.commit()
        except exc.IntegrityError as e: #Error si el jugador ya existe en la bd
            db.session.rollback()
            return f"Error: {e}"
        return jsonify({"Mensaje": f"Agregado {nya} correctamente"})

    else: #method PUT, agregando equipos dirigidos y a que equipo pertenece
        dni = request.form.get("dni")
        equipo_dirigido_form = request.form.get("equipo_dirigido")
        equipo_donde_juega_form = request.form.get("equipo")
        jugador = Jugador.query.filter_by(dni=dni).first()
        return "En construccion"
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