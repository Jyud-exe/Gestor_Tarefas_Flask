from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from wtforms.validators import DataRequired
from datetime import date, timedelta
from mod.models import Tarefas
from mod import db

class TarefasForm(FlaskForm):
    data = DateField()
    time = StringField(validators=[DataRequired()], render_kw={"placeholder": "HH:MM"})
    tarefa = StringField('', validators=[DataRequired()])
    btn = SubmitField('Adicionar')

    def save(self):
        nova_tarefa = Tarefas(
            data=self.data.data,
            time=self.time.data,
            tarefa=self.tarefa.data
        )

        db.session.add(nova_tarefa)
        db.session.commit()
        return nova_tarefa
    
    def Hoje(self):
        tarefas = Tarefas.query.order_by(Tarefas.time.asc())
        hoje = {}
        for t in tarefas:
            if t.data == date.today():
                data = t.data.strftime('%d/%m/%Y')
                if data not in hoje:
                    hoje[data] = []
                hoje[data].append(t)
        return hoje
    
    def Amanha(self):
        tarefas = Tarefas.query.order_by(Tarefas.time.asc())
        amanha = {}
        for t in tarefas:
            if t.data == date.today() + timedelta(days=1):
                data = t.data.strftime('%d/%m/%Y')
                if data not in amanha:
                    amanha[data] = []
                amanha[data].append(t)
        return amanha
    
    def agrupadas(self):
        tarefas = Tarefas.query.order_by(Tarefas.time.asc())
        agrupadas = {}
        for t in tarefas:
            data = t.data.strftime('%d/%m/%Y')
            if data not in agrupadas:
                agrupadas[data] = []
            agrupadas[data].append(t)
        return agrupadas

   