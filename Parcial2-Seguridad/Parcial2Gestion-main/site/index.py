from flask import Flask, render_template, request, session, redirect, url_for, g
from llaves import *
import smtplib
import random
from functions import *

class Usuario:
    def __init__(self, id, email, password, name, age, lastname, description, username=""):
        self.id = id
        self.email = email
        self.password = password
        self.name = name
        self.lastname = lastname
        self.description = description
        self.age = age
        self.username = username

    def __repr__(self) -> str:
        return f'Usuario:{self.email}>'


usuarios = []
usuarios.append(Usuario(id=1, email='clarissa@email.com', name='Clarissa', lastname='Martinez', password='cm1234',age=21, 
                description='Soy ingeniera en desarrollo de software', username='@cm_0'))
usuarios.append(Usuario(id=2, email='yansi@email.com', name='Yansi', lastname="Galdamez", password='ym1234', age=25,
                description='Soy mercadologa de CEPA', username='@galdamez_yansi'))
usuarios.append(Usuario(id=3, email='fatima@email.com', name='Fatima', lastname='Herrera', password='fm1234', age=26,
                description='Soy maestra de profesion ', username='@fherrera'))
usuarios.append(Usuario(id=4, email='sebas@email.com', name='Sebastian', lastname='Beltran', password='sb1234', age=28,
                description='Soy administrador de empresas ', username='@sebasbeltran0'))
usuarios.append(Usuario(id=5, email='majo@email.com', name='Majo', lastname='Siguenza', password='ms1234', age=22,
                description='Soy estudiante de enfermeria', username='@mj_s'))
usuarios.append(Usuario(id=6, email='roberto@email.com', name='Roberto', lastname='Rodriguez', password='rb1234', age=25,
                description='Soy estudiante de ingenieria en sistemas computacionales', username='@robert_r'))
usuarios.append(Usuario(id=7, email='rodrigo@email.com', name='Rodrigo', lastname='Polanco', password='rp1234', age=26,
                description='Soy ingeniero civil', username='@rodripolanco'))
usuarios.append(Usuario(id=8, email='oscar@email.com', name='Oscar', lastname='Vaquero', password='ov1234', age=22,
                description='Soy estudiante de ingenieria industrial, en la Universidad Matias Delgado', username='@vaquero12'))
usuarios.append(Usuario(id=9, email='meli@email.com', name='Melissa', lastname="Gonzalez", password='mg1234', age=20,
                description='Soy fotografa aficionado, actualmente estoy estudiando la carrera de fotografia', username='@melig'))
usuarios.append(Usuario(id=10, email='fg14012013@hotmail.com', name='Fernanda', lastname='Garcia', password='fg1234', age=22,
                description='Soy estudiante de Ingenieria de Software en la Universidad Catolica de El Salvador', username='@fgarcia_0'))


app = Flask(__name__)
app.secret_key = '123456'


@app.before_request
def before_request():
    g.usuario = None
    if 'id_user' in session and 'logged_in' in session:
        usuario = [x for x in usuarios if x.id == session['id_user']][0]
        g.usuario = usuario


@app.route('/')
def index():
    return redirect("/login", code=302)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('id_user', None)
        email = request.form['email']
        password = request.form['password']
        usuario = [x for x in usuarios if x.email == email and x.password == password]
        if usuario:
            session['id_user'] = usuario[0].id
            session['logged_in'] = True
            return redirect("/perfil", code=302)
        else:
            return render_template('login.html', error=True)
    else:
        if g.usuario:
            return redirect("/perfil", code=302)
        else:
            return render_template('login.html', error=False)


@app.route('/logout')
def logout():
    session.pop('id_user', None)
    session.clear()
    return redirect("/login", code=302)


@app.route('/perfil')
def perfil():
    if g.usuario == None:
        return redirect(url_for('login'))
    return render_template('perfil.html')

@app.route('/send_code', methods=['POST' , 'GET'])
def scode():
    if request.method == 'POST':
        session.pop('id_user', None)
        email = request.form['email']
        usuario = [x for x in usuarios if x.email == email]
        if usuario:
            session['id_user'] = usuario[0].id
            session['email'] = usuario[0].email
            otp = random.randint(1000,10000)
            session['otp'] = otp
            """ return str(session['otp']) + " " + session['email'] """
            can = send_email(otp,usuario[0].email)
            if can:
                return redirect("/code_verify", code=302)
            else:
                return 'Error'
                return redirect("/login", code=302)
        else:
            return redirect('/send_code', code=302)
    else:
        if g.usuario:
            return redirect("/perfil", code=302)
        else:
            return render_template('code_email.html', error=False)

@app.route('/code_verify', methods=['POST' , 'GET'])
def code_verify():
    if request.method == 'POST':
        code = request.form['code']
        print(code)
        print(session['otp'])
        if str(code) == str(session['otp']):
            session['logged_in'] = True
            print('llega')
            return redirect("/perfil", code=302)
        else:
            return redirect("/code_verify", code=302)
    else:
        if g.usuario:
            return redirect("/perfil", code=302)
        else:
            return render_template('code_verify.html', error=False)

@app.route('/oauth_login', methods=['GET', 'POST'])
def github_login():
    if g.usuario:
        return redirect("/perfil", code=302)
    else:
        return redirect("https://github.com/login/oauth/authorize?client_id=74e4780ee00bdf0ef199&scope=respo", code=302)

@app.route('/oauth_callback', methods=['GET', 'POST'])
def github_callback():
    if g.usuario:
        return redirect("/perfil", code=302)
    else:
        if  request.method == 'GET':
            session.pop('id_user', None)
            email = 'kokirene@hotmail.com'
            password = 'marcopass'
            usuario = [x for x in usuarios if x.email == email and x.password == password]
        if usuario:
            session['id_user'] = usuario[0].id
            session['logged_in'] = True
            code = request.args.get('code')
            print(code)
            return redirect("/perfil", code=302)     
    
"""  """

if __name__ == '__main__':
    app.run(debug=True)


