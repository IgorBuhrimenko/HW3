from flask import Flask, render_template
import requests
import sqlite3 as sq
from flask import g

app = Flask(__name__)
DATABASE = 'database.db' # Путь к базе данных


def get_db():  # Function get database
    db = getattr(g, '_database', None)
    if db is None:
        conn = sq.connect(DATABASE)  # Подключает базу данных
        conn.row_factory = sq.Row  # Возвращает строки
        db = g._database = conn
    return db


@app.teardown_appcontext # На момет сбоя сервера закрывет базу данных
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def index():
    return "Добро пожаловать в обменник"


<<<<<<< HEAD
def get_in_database(currency_to, exchange_rate, amount, results):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
                       insert into exchange (currency_to,exchange_rate,amount,results)
                           values (?, ?, ?, ?)
                   """, (currency_to, exchange_rate, amount, results))
    conn.commit()
=======
def write_to_file(*args):
    f = open('history.txt','a')
    list_elem = [str(x) for x in [*args]]
    if len(list_elem) == 4:
        f.write(','.join(list_elem))
        f.write("\n")
        f.close
>>>>>>> 3ab3cea6c9848e07e0c4a2bf15ac9e5f0cb77eba


def load_rate():
    r = requests.get('https://api.exchangeratesapi.io/latest')
    response_json = r.json()
    rates = response_json['rates']
    return rates


def get_cursor():
    conn = get_db()
    cursor = conn.cursor()
    return cursor


@app.route("/eur_to_usd/<int:amount>/")
def eur_to_usd(amount):
    exchange_rate = load_rate()['USD']
    results = amount * exchange_rate
    currency_to = 'usd'
    get_in_database(currency_to, exchange_rate, amount, results)
    return f"У вас {amount} EUR  , это {results} USD"


@app.route("/eur_to_gbp/<int:amount>/")
def eur_to_gbp(amount):
    exchange_rate = load_rate()['GBP']
    results = amount * exchange_rate
    currency_to = 'gbp'
    get_in_database(currency_to, exchange_rate, amount, results)
    return f"У вас {amount} EUR  , это {results} GBP"


@app.route("/eur_to_php/<int:amount>/")
def eur_to_php(amount):
    exchange_rate = load_rate()['PHP']
    results = amount * exchange_rate
    currency_to = 'php'
    get_in_database(currency_to, exchange_rate, amount, results)
    return f"У вас {amount} EUR  , это {results} PHP"


@app.route('/history/')
def history():
    cursor = get_cursor()
    cursor.execute(
        """select currency_to,exchange_rate,amount,results 
         from exchange"""
    )
    rows = cursor.fetchall()
    return render_template('history.html', rows=rows)


@app.route('/history/currency/<to_currenty>/')
def sort_sql(to_currenty):
    cursor = get_cursor()
    cursor.execute(
        """SELECT currency_to, exchange_rate, amount , results FROM exchange WHERE currency_to = ?""", (to_currenty,)
    )
    rows = cursor.fetchall()
    return render_template('currency.html', rows=rows)


@app.route('/history/amount_gte/<int:number>/')
def get_amount_gte(number):
    cursor = get_cursor()
    cursor.execute("SELECT amount FROM exchange WHERE amount >= ?", (number,))
    rows = cursor.fetchall()
    return render_template('amount111.html', rows=rows)


@app.route('/history/statistic')
def get_statistic():
    cursor = get_cursor()
    cursor.execute("""SELECT currency_to, count(currency_to),sum(results)
    FROM exchange GROUP BY currency_to
    """)
    rows = cursor.fetchall()
    return render_template('statistic.html', rows=rows)


def init_db():  # Инициализация БД
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


if __name__ == "__main__":
<<<<<<< HEAD
    init_db()
    app.run(debug=True)
=======
    app.run(debug=True)
>>>>>>> 3ab3cea6c9848e07e0c4a2bf15ac9e5f0cb77eba
