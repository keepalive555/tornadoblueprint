#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
import tornado.ioloop
import tornado.httpserver

from tornadoblueprint.blueprint import Blueprint
from tornadoblueprint.blueprint import HotPlugApplication


indexbp = Blueprint(__name__, prefix='/home')
indexbp.hotplug = True  # try False.


@indexbp.route('/welcome')
class IndexHanlder(tornado.web.RequestHandler):

    def get(self):
        return self.write("Hello TornadoBlueprint.")


if __name__ == '__main__':
    app = HotPlugApplication()
    app.register_blueprints()
    server = tornado.httpserver.HTTPServer(app)
    server.listen(8000)
    tornado.ioloop.IOLoop.current().start()
