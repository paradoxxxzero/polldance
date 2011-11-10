#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2011 by Florian Mounier, Kozea
# This file is part of polldance licensed under a 3-clause BSD license.

from gevent import monkey
monkey.patch_all()
import gevent.wsgi
import werkzeug.serving
from gevent.event import Event
from flask import Flask, render_template, jsonify, request


class Poll(object):

    def __init__(self):
        self.points = []
        self.event = Event()

    def add(self, message):
        self.points.append(message)
        self.event.set()
        self.event.clear()

    def clear(self):
        self.points = []
        self.event.set()
        self.event.clear()

    def wait(self):
        self.event.wait()


def make_app():
    app = Flask(__name__)
    poll = Poll()

    @app.route('/')
    def index():
        return render_template('index.jinja2')

    @app.route('/get/<int:last>')
    def get(last):
        if last > len(poll.points):
            last = 0
        if last != 0:
            poll.wait()
        return jsonify(points=poll.points[last:], last=len(poll.points))

    @app.route('/set', methods=['POST'])
    def set():
        poll.add({
            'x': request.values['x'],
            'y': request.values['y'],
            'c': request.values['c']})
        return jsonify(success=True)

    @app.route('/clear')
    def clear():
        poll.clear()
        return jsonify(success=True)

    return app


def run_server():
    app = make_app()
    ws = gevent.wsgi.WSGIServer(('', 1789), app)
    ws.serve_forever()


if __name__ == '__main__':
    run_server()
