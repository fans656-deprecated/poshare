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
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int)
    args = parser.parse_args()
    port = args.port or 6560

    app.run(host='0.0.0.0', port=port, debug=True)
