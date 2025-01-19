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
        equipos = Equipo.query.all()
        if len(equipos) > 0:
            return {"equipos": [equipo.to_json() for equipo in equipos]},200
        else:
            return jsonify({"Mensaje":"No hay equipos"}),204
        
    elif request.method == "POST":
        #Levantar valores del front
        data = request.json
        nombre = data.get("nombre")
        contacto = data.get("contacto")
        division = data.get("division")
        fecha_ingreso = date.fromisoformat(data.get("fechaIngreso")) #convertir string en un objeto date
        entrenador_id = data.get("entrenador")

        #Validar valores
        if validar_division_equipo(division) and validar_nombre(nombre) and validar_fecha(fecha_ingreso):
            #agregar equipo a la bd
            nuevo_equipo = Equipo(nombre=nombre, fecha_ingreso=fecha_ingreso,contacto=contacto, division=division,entrenador_id=entrenador_id)
            try:
                db.session.add(nuevo_equipo)
                db.session.commit()
            except exc.IntegrityError as e:
                db.session.rollback()
                return f"Error: {e}"
            return nuevo_equipo.to_json(),200
        else:
            return jsonify({"mensaje": "Error en los parametros"})
    else: # metodo PUT
        data = request.json
        nombre = data.get("nombre")
        dni = data.get("dni")
        division = data.get("division")
        nro_camiseta = data.get("nroCamiseta")
        posicion = data.get("posicion")
        categoria = data.get("categoria")

        jugador = Jugador.query.filter_by(dni=dni).first()
        equipo = Equipo.query.filter_by(nombre=nombre,division=division).first()
        if jugador is None or equipo is None:
            return {"mensaje":"Equipo o jugador no existen"}
        asociacion = JugadorEquipo(dni_jugador=jugador.dni, id_equipo=equipo.id,categoria=categoria, nro_camiseta=nro_camiseta,posicion=posicion)
        db.session.add(asociacion)
        try:
            db.session.commit()
        except exc.IntegrityError as e:
            return f"{e}"
        return asociacion.to_json(),200
    
@views.route("/eliminar_equipo/<int:id>", methods=["DELETE"])
def eliminar_equipo(id):
    try:
        equipo_a_eliminar = Equipo.query.filter_by(id=id).first()
        if equipo_a_eliminar is None:
            return jsonify({"mensaje":"No existe equipo con ese ID"})
        db.session.delete(equipo_a_eliminar)
        db.session.commit()
    except Exception as e:
        return jsonify({"mensaje":str(e)})
    return jsonify({"mensaje":f"Equipo {equipo_a_eliminar.nombre} eliminado correctamente"})

@views.route("/jugadores", methods=["GET","POST","PUT"])
def jugadores():
    if request.method == "GET":
        jugadores = Jugador.query.order_by(Jugador.dni).all()
        if len(jugadores) > 0:
            return {"jugadores": [jugador.to_json() for jugador in jugadores]},200
        else:
            return {"mensaje":"No hay jugadores"},204

    elif request.method == "POST":
        #Levantando info del jugador del front
        data = request.json
        dni = data.get("dni")
        nya = data.get("nya")
        sexo = data.get("sexo")
        telefono = data.get("telefono")
        fecha_nac = date.fromisoformat(data.get("fechaNac"))
        direccion = data.get("direccion")
        #creacion de jugador
        nuevo_jugador = Jugador(dni=dni,nya=nya,sexo=sexo,telefono=telefono,fecha_nac=fecha_nac,direccion=direccion)
        
        try:
            db.session.add(nuevo_jugador)
            db.session.commit()
        except exc.IntegrityError as e: #Error si el jugador ya existe en la bd
            db.session.rollback()
            return f"Error: {e}"
        return jsonify({"Mensaje": f"Agregado {nya} correctamente"})

    else: #method PUT, agrega equipo dirigido, REVISAR que tan necesario es
        dni = request.form.get("dni")
        equipo_a_dirigir_form = request.form.get("equipo_a_dirigir")
        equipo_donde_juega_form = request.form.get("equipo_donde_juega")
        jugador = Jugador.query.filter_by(dni=dni).first()
        
        #consiguiendo el equipo a dirigir
        equipo_a_dirigir = Equipo.query.get(equipo_a_dirigir_form)
        #consiguiendo el equipo donde juega
        equipo_donde_juega = Equipo.query.get(equipo_donde_juega_form)
        

        if equipo_donde_juega is not None and equipo_a_dirigir.nombre == equipo_donde_juega.nombre:
            return jsonify({"mensaje":"No podes dirigir y jugar en el mismo equipo"})
        jugador.equipo_dirigido = equipo_a_dirigir
        db.session.commit()
        return jsonify({"mensaje":f"Jugador {jugador.nya} se volvio entrenador de {equipo_a_dirigir.nombre}"})


@views.route("/eliminar_jugador/<int:dni>", methods=["DELETE"])
def eliminar_jugador(dni):
    try:
        jugador_a_eliminar = Jugador.query.filter_by(dni=dni).first()
        if jugador_a_eliminar is None:
            return jsonify({"mensaje":"No existe un jugador con ese id"}),404
        db.session.delete(jugador_a_eliminar)
        db.session.commit()
    except Exception as e:
        return jsonify({"mensaje":str(e)}),500
    return jsonify({"mensaje":"Jugador eliminado correctamente"})

@views.route("/ver_asociaciones",methods=["GET"])
def ver_asociaciones():
    asociaciones = JugadorEquipo.query.order_by(JugadorEquipo.id_equipo).all()
    return {"asociaciones":[asociacion.to_json() for asociacion in asociaciones]},200