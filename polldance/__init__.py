#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2014 by Florian Mounier, Kozea
# This file is part of polldance licensed under a 3-clause BSD license.


import os
import tornado.web
import tornado.websocket
import tornado.process
import tornado.ioloop
import tornado.options


class Index(tornado.web.RequestHandler):
    def get(self):
        return self.render('index.html')


class WebSocket(tornado.websocket.WebSocketHandler):
    clients = []
    buffer = []

    def open(self):
        WebSocket.clients.append(self)
        for message in WebSocket.buffer:
            self.write_message(message)

    def on_message(self, message):
        WebSocket.buffer.append(message)
        self.broadcast(message)

    def on_close(self):
        WebSocket.clients.remove(self)

    def broadcast(self, message):
        for client in WebSocket.clients:
            try:
                client.write_message(message)
            except Exception:
                WebSocket.clients.remove(client)


app = tornado.web.Application(
    [
        (r'/', Index),
        (r'/ws', WebSocket)
    ],
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    debug=tornado.options.options.debug
)
