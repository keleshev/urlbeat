import os
import tempfile

from pytest import fixture

import urlbeat


@fixture
def app():
    """Fixture that provides `app` with empty SQLite database."""
    db_fd, db_path = tempfile.mkstemp()
    urlbeat.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
    urlbeat.db.create_all()
    yield urlbeat.app.test_client()
    os.close(db_fd), os.unlink(db_path)


def test_urlbeat(app):
    """Create redirection to google.com, then test that it redirects."""
    assert app.get('/1').status == '404 NOT FOUND'
    assert app.post('/', data={'url': 'google.com'}).status == '200 OK'
    assert app.get('/1').status == '301 MOVED PERMANENTLY'
    assert app.get('/1').headers['Location'] == 'http://google.com'
