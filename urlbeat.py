import os

from flask import Flask, request, redirect, render_template as render
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)


def shorten(url):
    return 'http://short.url'


def lengthen(url):
    return 'http://google.com'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        return render('index.html', url=url, short_url=shorten(url))
    else:
        return render('index.html')


@app.route('/<key>')
def index_key(key):
    return redirect(lengthen(key))
