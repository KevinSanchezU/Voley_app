from flask import Blueprint, request, render_template
from .models import Equipo, Jugador

views = Blueprint("views", __name__)

def validar_equipo(equipo):
    if equipo.divison not in ["Sub-18", "Sub-21", "Mayores"]:
        return False
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
        #Equipo.query.all()
        return "<h1>Todos los equipos!</h1>"
    else:
        equipo = request.form.get("equipo")
        if validar_equipo(equipo=equipo) == True:
            #
            return "POST REQUEST"

@views.route("/jugadores")
def jugadores():
    #funcion que muestra todos los jugadores
    #Jugador.query.all()
    return "<h1>Todos los jugadores!</h1>"