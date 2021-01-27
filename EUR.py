from flask import Flask , render_template
import requests

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


def write_to_file(*args):
    f = open('history.txt','a')
    list_elem = [str(x) for x in [*args]]
    if len(list_elem) == 4:
        f.write(','.join(list_elem))
        f.write("\n")


def load_rate():
    r = requests.get('https://api.exchangeratesapi.io/latest')
    response_json = r.json()
    rates = response_json['rates']
    return rates


@app.route("/eur_to_usd/<int:amount>")
def eur_to_usd(amount):
    exchange_rate = load_rate()['USD']
    results = amount * exchange_rate
    currency_to = 'USD'
    write_to_file(currency_to, exchange_rate, amount, results)
    return f"У вас {amount} EUR  , это {results} USD"


@app.route("/eur_to_gbp/<int:amount>")
def eur_to_gbp(amount):
    exchange_rate = load_rate()['GBP']
    results = amount * exchange_rate
    currency_to = 'GBP'
    write_to_file(currency_to, exchange_rate, amount, results)
    return f"У вас {amount} EUR  , это {results} GBP"


@app.route("/eur_to_php/<int:amount>")
def eur_to_php(amount):
    exchange_rate = load_rate()['PHP']
    results = amount * exchange_rate
    currency_to = 'PHP'
    write_to_file(currency_to, exchange_rate, amount, results)
    return f"У вас {amount} EUR  , это {results} PHP"


@app.route('/history')
def history():
    f = open('history.txt', 'r')
    fr = f.readlines()
    f.close()
    return render_template('history.html', tex=fr)


if __name__ == "__main__":
    app.run(debug=True)