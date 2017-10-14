import string
import random

from bottle import Bottle, run
from bottle import mako_view as view, static_file
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
    id = gen_id()
    return dict(id=id)


@app.get('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root='./static')


if __name__ == '__main__':
    run(app, host='localhost', port=8080, debug=True)