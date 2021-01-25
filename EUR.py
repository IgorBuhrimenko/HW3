from flask import Flask , render_template
app = Flask(__name__)
import requests


response = requests.get('https://api.exchangeratesapi.io/latest')
response_json = response.json()
rates = response_json['rates']


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/eur_to_usd/<int:amount>")
def eur_to_usd(amount):
    exchange_rate = rates['USD']
    results = amount * exchange_rate
    currency_to = 'USD'
    f = open('history.txt','a')
    f.write(f"\n{currency_to} , {exchange_rate}, {amount}, {results} ")
    f.close()
    return f"У вас {amount} EUR  , это {results} USD"


@app.route("/eur_to_gbp/<int:amount>")
def eur_to_gbp(amount):
    exchange_rate = rates['GBP']
    results = amount * exchange_rate
    currency_to = 'GBP'
    f = open('history.txt','a')
    f.write(f"\n{currency_to} , {exchange_rate}, {amount}, {results} ")
    f.close()
    return f"У вас {amount} EUR  , это {results} GBP"


@app.route("/eur_to_php/<int:amount>")
def eur_to_php(amount):
    exchange_rate = rates['PHP']
    results = amount * exchange_rate
    currency_to = 'PHP'
    f = open('history.txt', 'a')
    f.write(f"\n{currency_to} , {exchange_rate}, {amount}, {results} ")
    f.close()
    return f"У вас {amount} EUR  , это {results} PHP"


@app.route('/history')
def history():
    f = open('history.txt')
    fr = f.readlines()
    return render_template('history.html', tex=fr)




if __name__ == "__main__":
    app.run(debug=True)
