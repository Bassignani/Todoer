import mysql.connector
import click #Es una herramienta que sirve para poder ejecutar comandos en la terminal
from flask import current_app, g #current_app mantiene la aplicacion que estamos ejecutando.
                                 #g es una variable que se encuentra en toda la aplicacion. Variable global. Lo vamos a usar para almacenar el usuario
from flask.cli import with_appcontext
from .schema import instructions  #archivo que va a contener todos los script que van a crear nuestra base de datos

def get_db():   #Funcion que genera la coneccion a la base de datos
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host=current_app.config['DATABASE_HOST'],   #Estos valores los debo definir por consola como "export FLASK_DATABASE_HOST='nombre_del_host'", y lo mismo para los atributos de abajo
            user=current_app.config['DATABASE_USER'],
            password=current_app.config['DATABASE_PASSWORD'],
            database=current_app.config['DATABASE']
        )
        g.c = g.db.cursor(dictionary=True)
    #print(current_app.config['DATABASE_HOST'])    #MUestra a que DB se esta conectando, dato que le pasamos por consola
    #print(current_app.config['DATABASE_USER'])
    #print(current_app.config['DATABASE_PASSWORD'])
    #print(current_app.config['DATABASE'])
    return g.db, g.c

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db, c = get_db()
    for i in instructions:
        c.execute(i)   # multi=True me permite insertar multiples consultas, sin eso da error.
    db.commit()    

@click.command('init-db')   #dede la terminal debo escribir "flask init-db" para que se ejecute esta funcion
@with_appcontext            #Este comando sirve para indicarle al script que use el contexto de la aplicacion, asi puede acceder a las variables de config
def init_db_command(): # Set de instrucciones parar ejecutar en sql
    init_db()  #Ejecuta la funcion  init_db que esta mas arriba
    click.echo('Base de datos inicializada')  #Lanza el cartel por la consola

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)