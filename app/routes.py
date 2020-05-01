from flask import render_template, request
from app import app, db
from app.forms import LoginForm, RegistrationForm
from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse
from sqlalchemy.sql import text
import pymysql.cursors
import pymysql
import csv
import time

import plotly.graph_objects as go

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username': 'Miguel'}
    posts = []
    return render_template('index.html', title='Home', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/stocks')
@login_required
def stocks():

    return render_template('stocks.html')

@app.route('/stocks/<company>')
@login_required
def stock_choose(company):

    return render_template('stock_choose.html', company = company)

@app.route('/stocks/<company>/<option>')
@login_required
def stock_plot(company, option):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 passwd='123',
                                 db='mydb',
                                 port=3306,
                                 cursorclass=pymysql.cursors.DictCursor)
    query = 'SELECT * FROM ' + company + '_' + option;
    cur = connection.cursor()
    cur.execute(query)
    result = cur.fetchall()

    fig = go.Figure()

    time = []
    open = []
    high = []
    low = []
    close = []
    volume = []
    for row in result:
        time.append(row['time'])
        open.append(row['open'])
        high.append(row['high'])
        low.append(row['low'])
        close.append(row['close'])
        volume.append(row['volume'])
    fig.add_trace(go.Scatter(x = time, y = open, name = 'open'))
    fig.add_trace(go.Scatter(x = time, y = high, name = 'high'))
    fig.add_trace(go.Scatter(x = time, y = low, name = 'low'))
    fig.add_trace(go.Scatter(x = time, y = close, name = 'close'))
    fig.show()
    fig.update_layout(title=company + ' ' + option + ' stock',
                      xaxis_title='Date',
                      yaxis_title='Price')

    return render_template('stock_plot.html', company = company, option = option)

