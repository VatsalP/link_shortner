import string
import random

from bottle import Bottle, run, request, redirect, abort
from bottle import mako_view as view, mako_template as template, static_file
from bottle.ext import sqlite

app = Bottle()
plugin = sqlite.Plugin(dbfile="./link_shortner.db")
app.install(plugin)


def gen_id(size=8, chars=string.ascii_letters + string.digits):
    """ Generates link_id
    """
    return "".join(
        random.SystemRandom().choice(chars) for _ in range(size)
    )


@app.get('/')
@view('index.html')
def index():
    return dict()


@app.post('/')
def index(db):
    link = request.forms.get('link')
    print(link)
    generated_id = gen_id()
    #row = db.execute('SELECT * from links where link_id=?', generate_id).fetchone()
    db.execute("INSERT INTO links values (?, ?)", (generated_id, link))
    shortened = "localhost:8080/" + generated_id
    return template("index_with_link.html", short_link=shortened)


@app.get('/<id:re:[a-zA-Z0-9]{8}>')
def redirect_to(id, db):
    print(id)
    row = db.execute('SELECT * from links where link_id=?', (id, )).fetchone()
    print(row)
    if row:
        redirect(row[1])
    else:
        abort(404, "No page found")


@app.get('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root='./static')


if __name__ == '__main__':
    run(app, host='localhost', port=8080, debug=True)