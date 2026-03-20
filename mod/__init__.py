import flask_sqlalchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask import Flask
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer
from dotenv import load_dotenv
import os

load_dotenv('.env')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

mail = Mail(app)
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

db = flask_sqlalchemy.SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = '/login'


from mod.routes import home
from mod.models import Tarefas