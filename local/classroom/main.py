# coding: utf-8
from datetime import datetime, timedelta
from flask import Flask, g, render_template, jsonify, request
from flask.ext.cors import CORS

app = Flask(__name__) # 创建flask实例
CORS(app) # 允许跨域访问

from db import create_tables, get_cursor, to_array
create_tables()

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/buildings')
def buildings():
    cur = get_cursor()
    cur.execute('select distinct building from rooms')
    r = cur.fetchall()
    return jsonify({'buildings': to_array(r)})

@app.route('/floors')
def floors():
    cur = get_cursor()
    building = request.args.get('building')
    cur.execute('select distinct floor from rooms where building = ?', (building,))
    return jsonify({
        'building': building,
        'floors': to_array(cur.fetchall())})

@app.route('/rooms')
def rooms():
    cur = get_cursor()
    building = request.args.get('building')
    floor = request.args.get('floor')
    cur.execute('select room from rooms where building = ? and floor = ?', (building, floor))
    return jsonify({
        'building': building,
        'floor': floor,
        'rooms': to_array(cur.fetchall())
        })

@app.route('/lessons')
def lessons():
    cur = get_cursor()
    building = request.args.get('building')
    room = int(request.args.get('room'))
    date = datetime.strptime(request.args.get('date'), '%Y-%m-%d')
    weekday = date.isoweekday()
    cur.execute('select * from lessons where building = ? and room = ? and weekday = ?',
            (building, room, weekday))
    r = cur.fetchall()
    r = [dict(zip(('lesson', 'teacher', 'building', 'floor', 'room', 'weekday', 'beg', 'end'), t))
            for t in r]
    for t in r:
        t['date'] = date.strftime('%Y-%m-%d')
        del t['weekday']
    return jsonify({'lessons': r})

@app.route('/rooms-of-lesson')
def rooms_of_lesson():
    cur = get_cursor()
    lesson = request.args.get('lesson')
    date = request.args.get('date')
    weekday = datetime.strptime(date, '%Y-%m-%d').isoweekday()
    cur.execute('select building, room, teacher, beg, end from lessons where lesson = ? and weekday = ?',
            (lesson, weekday))
    r = cur.fetchall()
    r = [dict(zip(('building', 'room', 'teacher', 'beg', 'end'), t))
            for t in r]
    return jsonify({'rooms': r, 'lesson': lesson})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6560, debug=True)
