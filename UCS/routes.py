from flask import Flask, Response, render_template, redirect, url_for, flash, request, abort, make_response
from UCS import app, database, bcrypt
from UCS.forms import FormLogin, FormContato
from UCS.models import Login, Contato
#from flask_login import login_user, logout_user, current_user, login_required
import pandas as pd
import io
import json
import flask_excel as excel

@app.route('/')
def home():
    return render_template('home.html')

# contato

@app.route('/contato/index', methods=['GET', 'POST'])
def contato_index():
    form = FormContato()
    if form.validate_on_submit():
        contato = Contato(nome = form.nome.data, sobrenome = form.sobrenome.data, email = form.email.data, telefone = form.telefone.data)
        database.session.add(contato)
        database.session.commit()
        return redirect("https://wa.me/5511982689581")
    return render_template('contato/index.html', form=form)


@app.route('/contato/create', methods=['GET', 'POST'])
#@login_required
def contato_create():
    form = FormContato()
    if form.validate_on_submit():
        contato = Contato(nome = form.nome.data, sobrenome = form.sobrenome.data, email = form.email.data, telefone = form.telefone.data)
        database.session.add(contato)
        database.session.commit()
        return redirect(url_for('contato_list'))
    return render_template('contato/create.html', form=form)


@app.route('/contato/delete/<row_id>', methods=['GET', 'POST'])
#@login_required
def contato_delete(row_id):
    form = FormContato()
    contato = Contato.query.get(row_id)
    if request.method == 'POST':
        database.session.delete(contato)
        database.session.commit()
        return redirect(url_for('contato_list'))
    return render_template('contato/delete.html', contato=contato, form=form)


@app.route('/contato/details/<row_id>')
#@login_required
def contato_details(row_id):
    form = FormContato()
    contato = Contato.query.get(row_id)
    return render_template('/contato/details.html', contato=contato, form=form)


@app.route('/contato/edit/<row_id>', methods=['GET', 'POST'])
#@login_required
def contato_edit(row_id):
    form = FormContato()
    contato = Contato.query.get(row_id)
    if request.method == 'GET':
        form.nome.data = contato.nome
        form.sobrenome.data = contato.sobrenome
        form.email.data = contato.email
        form.telefone.data = contato.telefone

    if request.method == 'POST':
        contato.nome = form.nome.data
        contato.sobrenome = form.sobrenome.data
        contato.email = form.email.data
        contato.telefone = form.telefone.data
        database.session.commit()
        return redirect(url_for('contato_list'))
    return render_template('/contato/edit.html', contato=contato, form=form)



@app.route('/contato/list')
#@login_required
def contato_list():
    form = FormContato()
    list_contatos = Contato.query.all()
    return render_template('/contato/list.html', list_contatos=list_contatos, form=form)


@app.route('/contato/list_estatica')
#@login_required
def contato_list_estatica():
    form = FormContato()
    list_contatos = Contato.query.all()
    return render_template('/contato/list_estatica.html', list_contatos=list_contatos, form=form)




@app.route('/list/contato_exportardados_excel', methods=['GET'])
#@login_required
def contato_exportardados_excel():
    list_contatos_objetos = Contato.query.all()
    list_contatos_json = [contato.to_json() for contato in list_contatos_objetos]
    df = pd.DataFrame(data=list_contatos_json, columns=('nome', 'sobrenome', 'email', 'telefone', 'data_criacao'))

    # Creating output and writer (pandas excel writer)
    out = io.BytesIO()
    writer = pd.ExcelWriter(out, engine='xlsxwriter')

    # Export data frame to excel
    df.to_excel(excel_writer=writer, index=False, sheet_name='Sheet1')
    writer.save()
    writer.close()

    # Flask create response
    r = make_response(out.getvalue())

    # Defining correct excel headers
    r.headers["Content-Disposition"] = "attachment; filename=export.xlsx"
    r.headers["Content-type"] = "application/x-xls"

    # Finally return response
    return r


# fim contato

# login

@app.route('/login/index', methods=['GET', 'POST'])
def login_index():
    form = FormLogin()
    mensagem = False
    if form.validate_on_submit():
        login_usuario = Login.query.filter_by(usuario=form.usuario.data).first()
        if login_usuario:
            # (login_usuario.senha, form.senha.data) verifica se são iguais
            if bcrypt.check_password_hash(login_usuario.senha, form.senha.data):
                #login_user(login_usuario)
                return redirect(url_for('contato_list'))
            else:
                mensagem = True
        else:
            mensagem = True
    return render_template('/login/index.html', form=form, mensagem=mensagem)


@app.route('/sair')
#@login_required
def sair():
    #logout_user()
    return redirect(url_for('home'))




@app.route('/login/create', methods=['GET', 'POST'])
#@login_required
def login_create():
    form = FormLogin()
    mensagem = False
    if form.validate_on_submit():
        login_usuario = Login.query.filter_by(usuario=form.usuario.data).first()
        if login_usuario:
            mensagem=True
        else:
            #Criptografar a senha
            senha_cript = bcrypt.generate_password_hash(form.senha.data)
            login = Login(usuario=form.usuario.data, senha=senha_cript)
            database.session.add(login)
            database.session.commit()
            return redirect(url_for('login_list'))
    return render_template('/login/create.html', form=form, mensagem=mensagem)



@app.route('/login/delete/<row_id>', methods=['GET', 'POST'])
#@login_required
def login_delete(row_id):
    form = FormLogin()
    login = Login.query.get(row_id)
    if request.method == 'POST':
        database.session.delete(login)
        database.session.commit()
        return redirect(url_for('login_list'))
    return render_template('login/delete.html', login=login, form=form)



@app.route('/login/edit/<row_id>', methods=['GET', 'POST'])
#@login_required
def login_edit(row_id):
    form = FormLogin()
    login = Login.query.get(row_id)
    if request.method == 'GET':
        form.usuario.data = login.usuario
        form.senha.data = login.senha
        return render_template('/login/edit.html', login=login, form=form)
    if request.method == 'POST':
        login.usuario = form.usuario.data
        login.senha = form.senha.data
        database.session.commit()
        return redirect(url_for('login_list'))


@app.route('/login/list')
#@login_required
def login_list():
    form= FormLogin()
    list_login = Login.query.all()
    return render_template('/login/list.html', list_login=list_login, form=form)

# fim login





