"""Urlbeat - simple URL shortener web app."""

import os
import string
from urlparse import urlparse, urlunparse

from flask import Flask, request, redirect, abort, render_template as render
from flask.ext.sqlalchemy import SQLAlchemy

from bda.basen import str2int, int2str


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)


class Redirection(db.Model):

    """Redirection as a resources.

    id:             Primary key.
    key:            Same as `id`, but encoded in base 62 with
                    numerals consisting of `alphabet` characters.
    alphabet:       String of allowed characters for short URLs.

    url:            URL which is redirected to.
    normalized_url: Same as `url` but converted to canonical
                    format and ensured that URL scheme (e.g. http)
                    is present.
    short_url:      Short URL constructed with `key`.

    """

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String)
    alphabet = string.digits + string.letters

    @property
    def key(self):
        return int2str(self.id, self.alphabet)

    @classmethod
    def for_key(self, key):
        return self.query.get(str2int(key, self.alphabet))

    @property
    def normalized_url(self):
        url = urlparse(self.url)
        if not url.scheme:
            url = urlunparse(['http', url.netloc, url.path,
                              url.params, url.query, url.fragment])
            return url.replace(':///', '://')  # Seems to be a `urlparse` bug.
        return self.url

    @property
    def short_url(self):
        return self.key and request.url_root + self.key


@app.route('/', methods=['GET', 'POST'])
def index():
    redirection = Redirection(url=request.form.get('url', ''))
    if request.method == 'POST' and redirection.url:
        db.session.add(redirection)
        db.session.commit()
    return render('index.html', redirection=redirection)


@app.route('/<key>')
def index_key(key):
    if set(key) <= set(Redirection.alphabet):
        redirection = Redirection.for_key(key)
        if redirection:
            return redirect(redirection.normalized_url)
    abort(404)


@app.errorhandler(404)
def page_not_found(error):
    return render('404.html'), 404
