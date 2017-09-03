#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
import tornado.ioloop
import tornado.httpserver

from tornadoblueprint.blueprint import Blueprint
from tornadoblueprint.blueprint import (
    HotPlugApplication,
    get_plugged_in_routes,
)


indexbp = Blueprint(__name__, prefix='/home')


@indexbp.route('/welcome')
class HomeHandler(tornado.web.RequestHandler):

    def get(self):
        self.write("<h3>Hello TornadoBlueprint.<h3>")
        return self.finish()


def get_app1():
    app = tornado.web.Application()
    for host, rules in get_plugged_in_routes():
        app.add_handlers(host, rules)
    return app


def get_app2():
    app = HotPlugApplication()
    app.register_blueprints()
    return app


if __name__ == '__main__':
    app = get_app1()
    server = tornado.httpserver.HTTPServer(app)
    server.listen(8000)
    tornado.ioloop.IOLoop.current().start()
