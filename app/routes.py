from flask import render_template, request, redirect, url_for, flash
from flask_login import (
    current_user,
    login_user,
    logout_user,
    login_required
)
from app import app, alquimias, db

@app.route("/")
# @login_required
def index():
    user = None
    if current_user.is_authenticated:
        user = current_user
        posts = alquimias.get_timeline()
    else:
        posts = []
    return render_template(
        'index.html',
        title = 'Página Inicial',
        user = user,
        posts = posts
    )

@app.route("/login", methods =['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username'].lower()
        password = request.form['password'].lower()

        user = alquimias.validate_user_password(username, password)
        if user:
            print("Login bem sucedido!")
            login_user(user, remember=user.remember)
            return redirect(url_for('index'))
        else:
            print('Usuário ou senha inválidos')
            return redirect(url_for('login'))
    
    return render_template('login.html')


@app.route('/cadastro', methods = ['POST','GET'])
def cadastro():
    if request.method == 'POST':
        username = request.form['username'].lower()
        if alquimias.user_exists(username):
            print('\n Usuário já existe \n')
            return redirect(url_for('login'))
        else:
            username = username
            remember = True if request.form.get('remember') == 'on' else False
            password = request.form.get('password').lower()
            profilepic = request.form.get('profilepic')
            bio= request.form.get('bio')

            user = alquimias.create_user(username, password, profilepic, bio)
            login_user(user, remember=remember)
            return redirect(url_for('index'))
    return render_template('cadastro.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/post', methods = ['GET', 'POST'])
@login_required
def post():
    if request.method == 'POST':
        body = request.form.get('body')
        alquimias.create_post(db.session, body, current_user.id)
        
        return redirect(url_for('index'))
    
    return render_template('post.html')
        



