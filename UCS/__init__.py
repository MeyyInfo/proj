from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import flask_excel as excel

app = Flask(__name__)

excel.init_excel(app)


app.config['SECRET_KEY'] = '8a26d65b8790442fd408667d3834d0ad'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bdsite.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login_index'
login_manager.login_message = 'Para acessar à página, faça o login.'
login_manager.login_message_category= 'alert-info'


from UCS import routes