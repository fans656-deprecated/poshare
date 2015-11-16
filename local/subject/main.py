# coding: utf-8
from datetime import datetime, timedelta
from flask import Flask, g, render_template, jsonify, request
from flask.ext.cors import CORS
from sqlalchemy.orm.exc import NoResultFound
from db import Subject, session, init_db

app = Flask(__name__) # 创建flask实例
CORS(app) # 允许跨域访问

# 主页
@app.route('/')
def root():
    return render_template('index.html')

# 查询所有的课程
@app.route('/subjects')
def subjects():
    r = [t.name for t in session.query(Subject.name).all()]
    return jsonify({'subjects': r})

# 查询某个课程的详细信息
@app.route('/description')
def description():
    name = request.args['name']
    r = session.query(Subject.description).filter(Subject.name == name).scalar()
    return jsonify({
        'name': name,
        'description': r
        })

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=6561, debug=True)
