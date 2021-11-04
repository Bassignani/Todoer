import functools  #Set de funciones que podemos utilizar cuando estamos construyendo aplicaciones

from flask import (  
    Blueprint, 
    flash,               #Permite mandar mensajes de manera generica a las plantillas
    g,                   #variable Global
    render_template,     #para renderizar plantillas
    request,             #Recibir datos de formulario
    url_for,             #Crear url
    session,              #Para mantener referancia del usuario en el contexto actual que se encuentra interactuando con la aplicacion
    redirect
)

from werkzeug.security import check_password_hash,generate_password_hash

from todo.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')  #Cualquier ruta que yo defina debajo va a estar concatenada coo /auth/....

@bp.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db, c = get_db()
        error = None
        c.execute(
            'select id from user where username = %s',
            (username,)
        )
        if not username:                        #Validamos los datos requeridos
            error = 'Username es requerido'
        if not password:
            error = 'Password es requerido'
        elif c.fetchone() is not None:          #Si el usuario existitee doy mensaje de error.
            error = 'El usuario {} se encuentra registrado.'.format(username)  #dentro de {} se coloca el username
        
        if error is None:                       #Si el usuario no existe lo creo 
            c.execute(
                'insert into user (username, password) values (%s,%s)',
                (username,generate_password_hash(password))   
            )    
            db.commit()

            return redirect(url_for('auth.login'))
        
        flash(error)
    
    return render_template('auth/register.html')


@bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db,c = get_db()
        error = None
        c.execute(
            'select * from user where username = %s',
            (username,)
        )
        user = c.fetchone()

        if user is None:   #Usuasrio incorrecto, pero digo que usuario/contraseña incorrecta asi un Hacker no sabe q el usuario existe o no
            error = 'Usuario y/o contrasenña invalidos'
        elif not check_password_hash(user['password'],password):   #contraseña incorrecta,pero digo que usuario/contraseña incorrecta asi un Hacker no sabe que la contraseña es incorrecta
            error = 'Usuario y/o contrasenña invalidos'

        if error is None:
            session.clear()  #limpiamos la sesion por posibles sesiones iniciadas     
            session['user_id'] = user['id']
            return redirect(url_for('todo.index'))

        flash(error)

    return render_template('auth/login.html')    

@bp.before_app_request   #Esta fiuncion se ejecuta antes de cada peticion
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        db, c = get_db()
        c.execute(
            'select * from user where id = %s',(user_id,)
        )    
        g.user = c.fetchone()


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)   
    return wrapped_view     

@bp.route('/loguot')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
