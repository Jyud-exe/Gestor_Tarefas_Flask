from flask_login import login_user, logout_user, login_required, current_user
from mod import app
from flask import render_template, redirect, url_for, request
from mod.forms import TarefasForm, LoginForm, cadForm
from mod.models import Tarefas
from datetime import date
from mod import db


@app.route('/', methods=['GET', 'POST'])
@login_required
def home(): 
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    form = TarefasForm()
    hoje = form.Hoje()
    amanha = form.Amanha() 
    lista = Tarefas.query.order_by(Tarefas.time.asc()).filter_by(user_tarefa=current_user.id).all()
    if form.validate and form.is_submitted():
        print('Formulário válido, salvando tarefa!')
        form.save()
        return redirect(request.referrer)
    cadform = cadForm()
    saudacao = cadform.saudacao()
    return render_template("index.html", 
        lista=lista, 
        form=form, 
        hoje=hoje, 
        amanha=amanha,
        saudacao=saudacao)

@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.btn.data and form.validate_on_submit():
        user = form.logar()
        if user:
            login_user(user, remember=True)
            return redirect(url_for('home'))
    return render_template('login.html', form=form)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    cadform = cadForm()
    if cadform.is_submitted() and cadform.validate():
        print('Formulário de cadastro válido, criando usuário!')
        user = cadform.save()
        login_user(user, remember=True)
        return redirect(url_for('home'))
    return render_template('cadastro.html', cadform=cadform)

@app.route('/delete/<int:id>')
def delete(id):
    tarefa = Tarefas.query.get(id)
    if tarefa:
        db.session.delete(tarefa)
        db.session.commit()
    if request.referrer:
        return redirect(request.referrer)
    return redirect(url_for('home')) 


@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    tarefa = Tarefas.query.get(id)
    if request.method == 'POST':
        tarefa.tarefa = request.form['titulo']
        tarefa.time = request.form['horario']
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('editar.html', tarefa=tarefa)


@app.route('/tarefas', methods=['GET', 'POST'])
def todas_tarefas():
    form = TarefasForm()
    agrupadas = form.agrupadas()
    return render_template('tarefas.html', agrupadas=agrupadas, form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

