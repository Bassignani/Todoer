import os #La libreria de os nos permite acceder a ciertas cosas del sistema operativo, como variables de entorno
from flask import Flask

def create_app():  #Es importante crear esta funcion cuando trabajamos en modulos para hacer testing o hacer varias instancias de nuestra app
    app = Flask(__name__) #Creamos el objeto de app para poder instanciar la clase FLask #Todas las aplicaciones que creamos en flask son una instancia de la clase Flask, y esta va a mantener un estado interno con distintas configuraciones de entorno y variables de usuario ect
    
    app.config.from_mapping(  #Permite definir variables de configuracion que vamos a utilizar en nuestra aplicacion
        SECRET_KEY = 'mikey', #Es una llave la cual se va a utilizat para poder definir las seciones(TOKEN/COOKIE) en nuestra aplicacion
        DATABASE_HOST = os.environ.get('FLASK_DATABASE_HOST'),  #obtengo las variables de entorno del sistema operativo
        DATABASE_PASSWORD = os.environ.get('FLASK_DATABASE_PASSWORD'),
        DATABASE_USER = os.environ.get('FLASK_DATABASE_USER'),
        DATABASE = os.environ.get('FLASK_DATABASE'),     #Estos valores los debo definir por consola como "export FLASK_DATABASE='nombre_de_db'", y lo mismo para los atributos de arriba
    )

    from . import db        #importa el archivo completo de la conexion a la base de datos 
    db.init_app(app) #Ejecuta la funicon de init_app 

    from .import auth
    app.register_blueprint(auth.bp)

    from .import todo
    app.register_blueprint(todo.bp)    


    @app.route('/hola')
    def hola():
        return 'Desde la app'
    
    return app