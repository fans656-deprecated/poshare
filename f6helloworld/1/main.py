# coding: utf-8
from flask import Flask

from routes import routes

app = Flask('server')

@app.route('/')
def root():
    return app.send_static_file('index.html')

for url, v in routes.items():
    func = v['func']
    app.route(url)(func)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6560, debug=True)
