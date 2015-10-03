# coding: utf-8
import os

from flask import Flask, g

app = Flask('server')

from routes import routes
from db import create_tables

#with app.app_context():
#    create_tables()

@app.teardown_appcontext
def close_connection(exception):
    t = getattr(g, '_database', None)
    if t is not None:
        t.close()

path = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(path, 'static/index.html')
index_html = open(path).read()

@app.route('/')
def root():
    return index_html

for url, v in routes.items():
    func = v['func']
    app.route(url)(func)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int)
    args = parser.parse_args()
    port = args.port or 6560

    app.run(host='0.0.0.0', port=port, debug=True)
