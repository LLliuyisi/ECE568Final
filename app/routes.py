from flask import render_template, request
from app import app, db
from app.forms import LoginForm, RegistrationForm
from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Portfolio
from werkzeug.urls import url_parse
from sqlalchemy.sql import text
from data.Data_Collection import getRealtime
from datetime import date, timedelta
import pymysql.cursors
import pymysql
import csv
import time

import plotly.graph_objects as go


company_names = {'FB': 'Facebook', 'MSFT': 'Microsoft', 'AMZN': 'Amazon', 'GOOG': 'Google',
                 'BRKB': 'Berkshire Hathaway', 'BRK-B': 'Berkshire Hathaway', 'AAPL': 'Apple',
                 'GE': 'General Electric', 'UBER': 'Uber', 'SBUX': 'Starbucks', 'COKE': 'Coca-Cola',
                 'NKE': 'Nike'}



@app.route('/')
@app.route('/index.html')
@login_required
def index():

    return render_template('index.html', companyname = company_names)

@app.route('/login.html', methods=['GET', 'POST'])
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

@app.route('/logout.html')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register.html', methods=['GET', 'POST'])
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

@app.route('/query.html')
@login_required
def query():



    data = {'FB': {},
            'MSFT': {},
            'AMZN': {},
            'GOOG': {},
            'NKE': {},
            'AAPL': {},
            'GE': {},
            'UBER': {},
            'SBUX': {},
            'COKE': {},
            }
    stocks = ['FB', 'MSFT', 'AMZN', 'GOOG', 'NKE', 'AAPL', 'GE', 'UBER', 'SBUX', 'COKE']
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 passwd='123',
                                 db='mydb',
                                 port=3306,
                                 cursorclass=pymysql.cursors.DictCursor)
    cur = connection.cursor()
    today_10 = str(date.today() - timedelta(days=10))
    today_365 = str(date.today() - timedelta(days=365))

    for stock in stocks:
        q = "SELECT MAX(open) FROM " + stock + "_historical where time > '" + today_10 + "'"
        cur.execute(q)
        result = cur.fetchone()
        #print(result)
        data[stock]['highest'] = float(result['MAX(open)'])

        q = "select open from " + stock + "_realtime ORDER BY time DESC LIMIT 1;"
        cur.execute(q)
        result = cur.fetchone()
        data[stock]['latest'] = float(result['open'])

        q = "SELECT MIN(open) FROM " + stock + "_historical where time > '" + today_365 + "'"
        cur.execute(q)
        result = cur.fetchone()
        data[stock]['lowest'] = float(result['MIN(open)'])

        q = "SELECT avg(open) FROM " + stock + "_historical where time > '" + today_365 + "'"
        cur.execute(q)
        result = cur.fetchone()
        data[stock]['average'] = round(float(result['avg(open)']), 2)

    #print (data)


    return render_template('query.html', data = data, companyname = company_names)

@app.route('/realtime.html<company>')
@login_required
def realtime(company):
    if company == "BRK-B":
        company = "BRKB"
    data = []
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 passwd='123',
                                 db='mydb',
                                 port=3306,
                                 cursorclass=pymysql.cursors.DictCursor)

    q = 'SELECT * FROM ' + company + '_realtime';
    cur = connection.cursor()
    cur.execute(q)
    result = cur.fetchall()

    for row in result:
        temp = []
        date, _time = row['time'].split(' ')
        year, month, day = date.split('-')
        hour, minute, second = _time.split(':')
        t = (int(year), int(month), int(day), int(hour), int(minute), int(second), 0, 0, 0)
        temp.append(int(time.mktime(t) * 1000.0))
        temp.append(float(row['open']))
        temp.append(float(row['high']))
        temp.append(float(row['low']))
        temp.append(float(row['close']))
        data.append(temp)
    print(data[0])


    return render_template('realtime.html', data=data, company=company)

@app.route('/predictions.html')
@login_required
def predictions():
    return render_template('predictions.html')

@app.route('/portfolio.html', methods=['GET', 'POST'])
@login_required
def portfolio():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 passwd='123',
                                 db='mydb',
                                 port=3306,
                                 cursorclass=pymysql.cursors.DictCursor)

    q = 'SELECT stockname FROM Portfolio WHERE userid = ' + current_user.get_id();
    cur = connection.cursor()
    cur.execute(q)
    result = cur.fetchall()
    stocks = []
    for row in result:
        if row['stockname'] == 'BRKB':
            stocks.append('BRK-B')
        else:
            stocks.append(row['stockname'])

    return render_template('portfolio.html', data = stocks, id = current_user.get_id(), companyname = company_names)

@app.route('/indicators.html<company>')
@login_required
def indicators(company):
    dates = []
    roc = []
    obv = []
    macd = []
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 passwd='123',
                                 db='mydb',
                                 port=3306,
                                 cursorclass=pymysql.cursors.DictCursor)

    q = 'SELECT * FROM ' + company + '_roc';
    cur = connection.cursor()
    cur.execute(q)
    result = cur.fetchall()
    for row in result:
        year, month, day = row['time'].split('-')
        t = (int(year), int(month), int(day), 0, 0, 0, 0, 0, 0)
        dates.append(int(time.mktime(t) * 1000.0))

        roc.append(float(row['indicator']))

    q = 'SELECT * FROM ' + company + '_obv';
    cur = connection.cursor()
    cur.execute(q)
    result = cur.fetchall()
    for row in result:
        obv.append(float(row['indicator']))

    q = 'SELECT * FROM ' + company + '_macd';
    cur = connection.cursor()
    cur.execute(q)
    result = cur.fetchall()
    for row in result:
        macd.append(float(row['indicator']))


    return render_template('indicators.html', company = company, time = dates, roc = roc, obv = obv, macd = macd)

@app.route('/historical.html<company>')
@login_required
def historical(company):
    data = []
    if company == "BRK-B":
        company = "BRKB"
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 passwd='123',
                                 db='mydb',
                                 port=3306,
                                 cursorclass=pymysql.cursors.DictCursor)

    q = 'SELECT * FROM ' + company + '_historical';
    cur = connection.cursor()
    cur.execute(q)
    result = cur.fetchall()

    for row in result:
        temp = []
        year, month, day = row['time'].split('-')
        t = (int(year), int(month), int(day), 0, 0, 0, 0, 0, 0)
        temp.append(int(time.mktime(t) * 1000.0))
        temp.append(float(row['open']))
        temp.append(float(row['high']))
        temp.append(float(row['low']))
        temp.append(float(row['close']))
        data.append(temp)
    print(data[0])

    return render_template('historical.html',data = data, company = company)

@app.route('/revise.html', methods=['GET', 'POST'])
@login_required
def revise():
    if request.method == 'POST':
        newStock = request.form.get('newStockName')
        if newStock == 'BRK-B':
            newStock = 'BRKB'

        stocks = ['FB', 'MSFT', 'AMZN', 'GOOG', 'NKE', 'AAPL', 'GE', 'UBER', 'SBUX', 'COKE']
        if newStock not in stocks:
            return render_template('error.html')

        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     passwd='123',
                                     db='mydb',
                                     port=3306,
                                     cursorclass=pymysql.cursors.DictCursor)
        
        q = 'SELECT stockname FROM Portfolio WHERE userid = ' + current_user.get_id();
        cur = connection.cursor()
        cur.execute(q)
        result = cur.fetchall()

        for row in result:
            if row['stockname'] == newStock:
                return render_template('error.html')
        portfolio = Portfolio(userid = current_user.get_id(), stockname = newStock)
        db.session.add(portfolio)
        db.session.commit()
        return render_template('success.html')
    return render_template('revise.html')

@app.route('/delete<company><userid>')
@login_required
def delete(company, userid):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 passwd='123',
                                 db='mydb',
                                 port=3306,
                                 cursorclass=pymysql.cursors.DictCursor)
    if company == 'BRK-B':
        company = 'BRKB'
    q = "DELETE FROM Portfolio WHERE userid = '" + userid + "' AND stockname = '" + company + "'";
    print (q)
    cur = connection.cursor()
    cur.execute(q)
    connection.commit()
    return redirect('portfolio.html')
'''
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
    q = 'SELECT * FROM ' + company + '_' + option;
    cur = connection.cursor()
    cur.execute(q)
    result = cur.fetchall()
    print (result[0])
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

    fig.update_layout(title=company + ' ' + option + ' stock',
                      xaxis_title='Date',
                      yaxis_title='Price')
    fig.write_html("app/templates/plot.html")
    return render_template('stock_plot.html', company = company, option = option)

@app.route('/query', methods=['GET', 'POST'])
@login_required
def query():
    if request.method == 'POST':  # this block is only entered when the form is submitted
        option = request.form.get('queries')
        if option == "showall":
            return render_template('query_response.html', cart = car)
        elif option == "companies":
            return render_template('query_response.html', cart=car)
        else:
            return render_template('query_response.html', cart=car)
    return render_template('query.html')



'''


