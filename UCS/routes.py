from flask import render_template, redirect, url_for
from Proj_UCS import app

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/sair')
def sair():
    return redirect(url_for('home'))