from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
# Biblioteca de validação dos campos
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from UCS.models import Contato
from flask_login import current_user


class FormLogin(FlaskForm):
    usuario = StringField('Usuário', validators =[DataRequired(message='Digite um nome de usuário válido')])
    senha = PasswordField('Senha', validators =[DataRequired(), Length(3, 20, message='Digite um valor para a senha de 3 a 20 caracteres') ])
    botao_submit = SubmitField('Fazer login Adm')


class FormContato(FlaskForm):
    nome = StringField('Nome', validators =[DataRequired(message='Digite o nome do usuário')])
    sobrenome = StringField('Sobrenome', validators =[DataRequired(message='Digite o sobrenome do usuário ')])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    telefone = StringField('Telefone', validators=[DataRequired(message='Digite um telefone válido')])
    botao_submit = SubmitField('Cadastrar Contato')

