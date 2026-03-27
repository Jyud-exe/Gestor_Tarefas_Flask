from flask_login import current_user, login_user
from flask import url_for, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, SubmitField, DateField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, email, Regexp, ValidationError
from datetime import date, timedelta, datetime
from mod.models import Tarefas, User
from flask_wtf import FlaskForm
from flask_mail import Message
from mod import db
import re

class TarefasForm(FlaskForm):
    data = DateField('Data')
    time = StringField('Horário', validators=[DataRequired()], render_kw={"placeholder": "HH:MM"})
    tarefa = StringField('Tarefa', validators=[DataRequired()], render_kw={"placeholder": "Tarefa"})
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
        tarefas = Tarefas.query.filter_by(user_tarefa=current_user.id).order_by(Tarefas.time.desc()).all()
        agrupadas = {}
        for t in tarefas:
            data = t.data.strftime('%d/%m/%Y')
            if data not in agrupadas:
                agrupadas[data] = []
            agrupadas[data].append(t)
        return agrupadas
    
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = StringField('Senha', validators=[DataRequired()])
    submit = SubmitField('Login')

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user:
            if check_password_hash(user.senha, self.senha.data):
                return login_user(user)
            else:
                raise ValidationError('Email ou senha incorretos!')
        else:
            raise ValidationError('Usuário não encontrado!')
        
        

class cadForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = StringField('Senha', validators=[DataRequired()])
    confirmar_senha = StringField('Confirmar Senha', validators=[DataRequired()])
    btn = SubmitField('Cadastrar')

    def senha_forte(self, senha):
        return(
            len(senha) >= 8 and
            re.search(r"[A-Z]", senha) and
            re.search(r"[a-z]", senha) and
            re.search(r"[\d]", senha) and
            re.search(r"[@#$%&]", senha))
            

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email já cadastrado!')
        
    def validate_senha(self, field):
        if not self.senha_forte(field.data):
            raise ValidationError('Senha Fraca!')

    def validate_confirmar_senha(self, field):
        if self.senha.data != field.data:
            raise ValidationError('Senhas devem ser iguais!')
       
    def save(self):
        Senha = generate_password_hash(self.senha.data)
        novo_usuario = User(
            nome=self.nome.data,
            email=self.email.data,
            senha=Senha,
            confirmado=False
        )
        db.session.add(novo_usuario)
        db.session.commit()
        return login_user(novo_usuario)


    def saudacao(self):
           hora = datetime.now().hour
           if hora < 12:
               return 'Bom dia,'
           if hora < 18:
               return 'Boa tarde,'
           if hora < 24:
               return 'Boa noite,'
           
    
            


    
   