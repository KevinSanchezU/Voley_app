from flask import Flask

def crear_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "this is a secret key, pero en espaniol"
    
    from .views import views

    app.register_blueprint(views,url_prefix="/")
    
    return app