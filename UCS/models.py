from UCS import database, login_manager
from datetime import datetime
from flask_login import UserMixin
import json


@login_manager.user_loader
def load_usuario(id_usuario):
    return Login.query.get(int(id_usuario))


class Login(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    usuario = database.Column(database.String, nullable= False)
    senha = database.Column(database.String, nullable=False)


class Contato(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String, nullable = False)
    sobrenome = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False)
    telefone = database.Column(database.String, nullable=False)
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)

    def to_json(self):
        return {'id': self.id, 'nome': self.nome, 'sobrenome': self.sobrenome, 'email': self.email, 'telefone': self.telefone,
                'Data Criação': self.data_criacao}


