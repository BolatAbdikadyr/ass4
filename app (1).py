from requests import Session
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from bs4 import BeautifulSoup
import json

app = Flask(name)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:sergazin@localhost/Assignment4'
app.config['SECRET_KEY'] = 'thisismyflasksecretkey'
db = SQLAlchemy(app)

class UserTable(db.Model):
    tablename = 'crypto'
    id = db.Column('id', db.Unicode, primary_key = True)
    coin_name = db.Column('coin_name', db.Unicode)
    short_name = db.Column('short_name', db.Unicode)

    def init(self, id, coin_name, short_name):
        self.id = id
        self.coin_name = coin_name
        self.short_name = short_name

soup = BeautifulSoup('main.html', 'html.parser')

def findCoinId(cryptoName):
    return db.session.query(UserTable.id).filter_by(coin_name=cryptoName).first()

html = """<div class=my_class><form action="{{ url_for('news') }}"><input type=text name=coinInput></input> <input type=submit value="Send Request"></input></form> <p>news text</p></div>"""

def findNews(cryptoName):
    url = 'https://api.coinmarketcap.com/content/v3/news?coin=' + str(findCoinId(cryptoName))

    parameters = {
        'slug': cryptoName,
        'convert':'USD'
    }

    headers = {
        'Accepts':'application/json',
        'X-CMC_PRO_API_KEY':'38334381-94e7-4f35-b5a7-7924dc4785c2'
    }

    session = Session()
    session.headers.update(headers)

    response = session.get(url, params=parameters)

    someVariable = json.loads(response.text)['data']
    print(type(someVariable))
    print(len(someVariable))
    i = 0
    listStrings = []
    for x in someVariable:
        listStrings.append(soup.get_text((x['meta']['content'])))
        print(listStrings[i])
        i = i + 1
        print("WE ARE HERE !!!!")
    return listStrings

@app.route('/')
def index():
    with open("C:/Users/SBatyrkhan/Desktop/4th/Python/learning/final/templates/main.html", 'r') as f:
        html_file_as_string = f.read()

    soup = BeautifulSoup(html_file_as_string, "lxml")

    for div in soup.find_all('div', {'class': 'my_class'}):
        for p in div.find('p'):
            p.string.replace_with('news text')

    with open('C:/Users/SBatyrkhan/Desktop/4th/Python/learning/final/templates/main.html', 'wb') as f:
        f.write(soup.renderContents())
    return render_template('main.html')

@app.route('/news')
def news():
    coin = request.args.get('coinInput')

    with open("C:/Users/SBatyrkhan/Desktop/4th/Python/learning/final/templates/main.html", 'r') as f:
        html_file_as_string = f.read()

    soup = BeautifulSoup(html_file_as_string, "lxml")

    finalList = findNews(coin)

    for div in soup.find_all('div', {'class': 'my_class'}):
        for x in finalList:
            div.find('p').string.replace_with(x)

    with open('C:/Users/SBatyrkhan/Desktop/4th/Python/learning/final/templates/main.html', 'wb') as f:
        f.write(soup.renderContents())

    #soup = BeautifulSoup("templates/main.html", "html.parser")

    return render_template('main.html')

if name == 'main':
    app.run(debug=True)
