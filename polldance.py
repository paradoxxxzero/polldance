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
        self.messages = []
        self.event = Event()

    def add(self, message):
        self.messages.append(message)
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
        if last != 0:
            poll.wait()
        return jsonify(points=poll.messages[last:], last=len(poll.messages))

    @app.route('/set', methods=['POST'])
    def set():
        poll.add({
            'x': request.values['x'],
            'y': request.values['y'],
            'c': request.values['c']
        })
        return jsonify(success=True)

    return app


@werkzeug.serving.run_with_reloader
def runServer():
    app = make_app()
    app.debug = True
    ws = gevent.wsgi.WSGIServer(('', 1789), app)
    ws.serve_forever()
