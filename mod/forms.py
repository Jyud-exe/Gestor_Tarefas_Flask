from flask_login import current_user
from flask import app, redirect, render_template, url_for, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, SubmitField, DateField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, email, Regexp
from datetime import date, timedelta, datetime
from mod.models import Tarefas, User
from flask_wtf import FlaskForm
from flask_mail import Message
from mod import db, serializer, mail

class TarefasForm(FlaskForm):
    data = DateField('Data')
    time = StringField('Horário', validators=[DataRequired()], render_kw={"placeholder": "HH:MM"})
    tarefa = StringField('Tarefa', validators=[DataRequired()])
    btn = SubmitField('Adicionar')

    def save(self):
        nova_tarefa = Tarefas(
             data=self.data.data,
             time=self.time.data,
             tarefa=self.tarefa.data,
             user_tarefa=current_user.id
        )
        db.session.add(nova_tarefa)
        db.session.commit()
        return nova_tarefa

    def Hoje(self):
        tarefas = Tarefas.query.filter_by(user_tarefa=current_user.id).order_by(Tarefas.time.asc()).all()
        hoje = {}
        for t in tarefas:
            if t.data == date.today():
                data = t.data.strftime('%d/%m/%Y')
                if data not in hoje:
                    hoje[data] = []
                hoje[data].append(t)
        return hoje
    
    def Amanha(self):
        tarefas = Tarefas.query.filter_by(user_tarefa=current_user.id).order_by(Tarefas.time.asc()).all()
        amanha = {}
        for t in tarefas:
            if t.data == date.today() + timedelta(days=1):
                data = t.data.strftime('%d/%m/%Y')
                if data not in amanha:
                    amanha[data] = []
                amanha[data].append(t)
        return amanha
    
    def agrupadas(self):
        tarefas = Tarefas.query.filter_by(user_tarefa=current_user.id).order_by(Tarefas.time.asc()).all()
        agrupadas = {}
        for t in tarefas:
            data = t.data.strftime('%d/%m/%Y')
            if data not in agrupadas:
                agrupadas[data] = []
            agrupadas[data].append(t)
        return agrupadas
    
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    btn = SubmitField('Login')

    def logar(self):
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            if check_password_hash(user.senha, self.senha.data):
                return user
            else:
                raise ValueError('Email ou senha incorretos!')
        else:
            raise ValueError('Usuário não encontrado!')
        

class cadForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Regexp(r'^(?=.*[a-zA-Z])(?=.*\d)(?=.*[@#$!%*?&]).{8,}$', message='Senha fraca!')])
    confirmar_senha = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('senha', message='As senhas devem ser iguais!')])
    btn = SubmitField('Cadastrar')

    def save(self):
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            raise ValueError('Email já cadastrado!')
        else:
            Senha = generate_password_hash(self.senha.data)
            novo_usuario = User(
                nome=self.nome.data,
                email=self.email.data,
                senha=Senha,
                is_verified=False
            )

            db.session.add(novo_usuario)
            token = serializer.dumps(self.email.data, salt='confirmar_email')
            link = url_for('confirmar_email', token=token, _external=True)
            msg = Message(
                subject='Confirme seu Email!',
                sender=current_app.config['MAIL_USERNAME'],
                recipients=[self.email.data]
                )
            msg.body = f'Clique no link para confirmar seu Email: {link}'
            mail.send(msg)
            return novo_usuario


    def saudacao(self):
           hora = datetime.now().hour
           if hora < 12:
               return 'Bom dia,'
           if hora < 18:
               return 'Boa tarde,'
           if hora < 24:
               return 'Boa noite,'
           
    
            


    
   