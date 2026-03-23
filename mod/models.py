from mod import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Tarefas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, default=db.func.current_date())
    time = db.Column(db.String, nullable=True)
    tarefa = db.Column(db.String, nullable=True)
    user_tarefa = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=True, unique=True)
    senha = db.Column(db.String)
    tarefa_id = db.relationship('Tarefas', backref='user', lazy=True)
    confirmado = db.Column(db.String, default='N')

    

    