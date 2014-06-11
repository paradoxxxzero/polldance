#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2011 by Florian Mounier, Kozea
# This file is part of polldance licensed under a 3-clause BSD license.

import tornado.options
import tornado.ioloop
import tornado.httpserver
import logging

tornado.options.define("debug", default=False, help="Debug mode")
tornado.options.define("host", default='localhost', help="Server host")
tornado.options.define("port", default=8273, type=int, help="Server port")

tornado.options.parse_command_line()


for logger in ('tornado.access', 'tornado.application',
               'tornado.general', 'miaou'):
    level = logging.WARNING
    if tornado.options.options.debug:
        level = logging.DEBUG
    logging.getLogger(logger).setLevel(level)

log = logging.getLogger('polldance')

log.info('Starting the dance')

from polldance import app

app.listen(tornado.options.options.port, tornado.options.options.host)

ioloop = tornado.ioloop.IOLoop.instance()
ioloop.start()
