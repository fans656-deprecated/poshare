# coding: utf-8
from datetime import datetime, timedelta

from flask import jsonify, request

from db import cur

def to_array(d):
    return [t.values()[0] for t in d]

def error(msg):
    return jsonify({'error': msg})

def buildings():
    cur.execute('select distinct building from rooms')
    r = cur.fetchall()
    return jsonify({'buildings': to_array(r)})

def floors():
    try:
        building = request.args.get('building').encode('utf-8')
    except AttributeError:
        return error('Require <building> to be specified.')
    cur.execute('select distinct floor from rooms where building = %s', (building,))
    return jsonify({
        'building': building,
        'floors': to_array(cur.fetchall())})

def rooms():
    try:
        building = request.args.get('building').encode('utf-8')
        floor = request.args.get('floor').encode('utf-8')
    except AttributeError:
        return error('Require <building> and <floor> to be specified.')
    cur.execute('select room from rooms where building = %s and floor = %s', (building, floor))
    return jsonify({
        'building': building,
        'floor': floor,
        'rooms': to_array(cur.fetchall())
        })

def lessons():
    try:
        building = request.args.get('building').encode('utf-8')
        room = request.args.get('room')
        date = request.args.get('date')
    except AttributeError:
        return error('Require <building> and <room> and <date> to be specified.')
    room = int(room)
    date = datetime.strptime(date, '%Y-%m-%d')
    weekday = date.isoweekday()
    cur.execute('select * from lessons where building = %s and room = %s and weekday = %s',
            (building, room, weekday))
    r = cur.fetchall()
    for t in r:
        t['date'] = date.strftime('%Y-%m-%d')
        del t['weekday']
    return jsonify({'lessons': r})

def rooms_of_lesson():
    lesson = request.args.get('lesson').encode('utf-8')
    date = request.args.get('date')
    weekday = datetime.strptime(date, '%Y-%m-%d').isoweekday()
    cur.execute('select building, room, teacher, beg, end from lessons where lesson = %s and weekday = %s',
            (lesson, weekday))
    r = cur.fetchall()
    print r
    return jsonify({'rooms': r, 'lesson': lesson})

routes = {
    '/buildings': {
        'func': buildings,
        'doc': {
            'desc': u'返回所有教学楼名称',
            'params': u'无',
            'return': u''''''
        }
    },

    '/floors': {
        'func': floors,
        'doc': {
            'desc': u'',
            'params': u'',
            'return': u''
        }
    },

    '/rooms': {
        'func': rooms,
        'doc': {
            'desc': u'',
            'params': u'',
            'return': u''
        }
    },

    '/lessons': {
        'func': lessons,
        'doc': {
            'desc': u'',
            'params': u'',
            'return': u''
        }
    },

    '/rooms-of-lesson': {
        'func': rooms_of_lesson,
        'doc': {
            'desc': u'',
            'params': u'',
            'return': u''
        }
    }
}
