import string
import random
import sqlite3

from bottle import Bottle, run, request, redirect, abort
from bottle import mako_view as view, static_file
from bottle_utils import csrf

app = Bottle()
app.config.load_config('./app.conf')

def gen_id(size=8, chars=string.ascii_letters + string.digits):
    """ Generates link_id
    """
    return "".join(
        random.SystemRandom().choice(chars) for _ in range(size)
    )


@app.get('/')
@view('index.html')
@csrf.csrf_token
def index():
    """ze index page 
    """
    return dict(csrf_tag=csrf.csrf_tag())


@app.post('/')
@view('index_with_link.html')
@csrf.csrf_protect
def index_with_links():
    """post request that the form link uses
    """
    db = sqlite3.connect('link_shortner.db')
    c = db.cursor()
    link = request.forms.get('link')
    generated_id = gen_id()
    #row = db.execute('SELECT * from links where link_id=?', generate_id).fetchone()
    c.execute("INSERT INTO links values (?, ?)", (generated_id, link))
    db.commit()
    db.close()
    shortened = "localhost:8080/" + generated_id
    return dict(short_link=shortened, csrf_tag=csrf.csrf_tag())


@app.get('/<id:re:[a-zA-Z0-9]{8}>')
def redirect_to(id):
    """redirects to the required link
    """
    db = sqlite3.connect('link_shortner.db')
    c = db.cursor()
    row = c.execute('SELECT * from links where link_id=?', (id, )).fetchone()
    db.close()
    if row:
        redirect(row[1])
    else:
        abort(404)


@app.get('/static/<filename:path>')
def send_static(filename):
    """Serve static files
    """
    return static_file(filename, root='./static')


@app.error('403')
@view('error/403.html')
def error403(error):
    """403
    """
    return dict()


@app.error('404')
@view('error/404.html')
def error404(error):
    """404
    """
    return dict()


if __name__ == '__main__':
    run(app, host='localhost', port=8080, debug=True)
