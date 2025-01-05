from flask import Blueprint, request, render_template

views = Blueprint("views", __name__)


@views.route("/")
def home():
    return "<h1> Bienvenido a la liga, elija si ver equipos o Jugadores</h1>"
@views.route("/equipos", methods=["GET","POST"])
def equipos():
    #funcion que muestra todos los equipos
    if request.method == "GET":
        return "<h1>Todos los equipos!</h1>"
    return "POST REQUEST"

@views.route("/jugadores")
def jugadores():
    #funcion que muestra todos los jugadores
    return "<h1>Todos los jugadores!</h1>"