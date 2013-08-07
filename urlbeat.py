import os
import string

from flask import Flask, request, redirect, abort, render_template as render
from flask.ext.sqlalchemy import SQLAlchemy

from bda.basen import str2int, int2str


alphabet = string.digits + string.letters
encode = lambda id: int2str(id, alphabet)
decode = lambda key: str2int(key, alphabet)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)


class Redirection(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String)

    @property
    def key(self):
        return encode(self.id)

    @property
    def short_url(self):
        return request.url_root + self.key


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        redirection = Redirection(url=url)
        db.session.add(redirection)
        db.session.commit()
        return render('index.html', redirection=redirection)
    else:
        return render('index.html')


@app.route('/<key>')
def index_key(key):
    redirection = db.session.query(Redirection).get(decode(key))
    if redirection:
        return redirect(redirection.url)
    else:
        abort(404)


#@app.errorhandler(404)
#def page_not_found(error):
#    return render('page_not_found.html'), 404
