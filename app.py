#!/usr/bin/env python
# -*- mode: python; -*-
# (c) 2013* Adam Stokes <hackr@cypherbook.com>

import os
import sys
import re
import logging
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.autoreload
from tornado.process import fork_processes, task_id
from tornado.log import app_log
from tornado.options import define, options, parse_command_line

commons = {}
commons['script_location'] = os.path.abspath(os.path.dirname(__file__))

sys.path.insert(0, commons['script_location'])

define("port", default=9000, help="port", type=int)
define("debug", default=False, help="run in debug mode", type=bool)

class RunApp(object):
    def __init__(self, commons):
        self.commons = commons
        self.commons['safe_mode'] = False
        parse_command_line()

    def run(self):
        if options.debug:
            app_log.setLevel(logging.DEBUG)

        if not options.debug:
            fork_processes(None)
        options.port += task_id() or 0

        app_log.debug("Starting %s on port %s" % ('tornado skeleton', options.port))
        # initialize the application
        tornado.httpserver.HTTPServer(Application(self.commons)).listen(options.port, '0.0.0.0')
        ioloop = tornado.ioloop.IOLoop.instance()
        if options.debug:
            tornado.autoreload.start(ioloop)
        # enter the Tornado IO loop
        ioloop.start()

class Application(tornado.web.Application):
    def __init__(self, commons):
        self.commons = commons
        app_log.debug("Application path (%s)" % (self.commons['script_location'],))

        urls = [
            (r"/(.*)", tornado.web.StaticFileHandler,
             {"path" : os.path.join(self.commons['script_location'],
                                    'app',
                                    'index.html')}),
            (r"/partials/(.*)", tornado.web.StaticFileHandler,
             {"path" : os.path.join(self.commons['script_location'],
                                    'app',
                                    'partials')}),

        ]

        settings = dict(
            template_path=None,
            static_path=os.path.join(self.commons['script_location'],
                                     'app'),
            xsrf_cookies=False if options.debug else True,
            cookie_secret='i love my dog!',
            debug=options.debug,
            )
        tornado.web.Application.__init__(self, urls, **settings)

if __name__=="__main__":
    sys.exit(RunApp(commons).run())
