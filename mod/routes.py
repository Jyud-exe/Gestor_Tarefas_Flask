from mod import app
from flask import render_template, redirect, url_for, request
from mod.forms import TarefasForm
from mod.models import Tarefas
from mod import db

@app.route('/', methods=['GET', 'POST'])
def home(): 
    form = TarefasForm()
    hoje = form.Hoje()
    amanha = form.Amanha()
    lista = Tarefas.query.order_by(Tarefas.time.asc())
    if form.validate and form.is_submitted():
        form.save()
        return redirect(url_for('home'))
    return render_template("index.html", lista=lista, form=form, hoje=hoje, amanha=amanha)


@app.route('/delete/<int:id>')
def delete(id):
    tarefa = Tarefas.query.get(id)
    if tarefa:
        db.session.delete(tarefa)
        db.session.commit()
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
