#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
import tornado.ioloop
import tornado.httpserver

from tornadoblueprint import blueprint


indexbp = blueprint.Blueprint(__name__, prefix='')


@indexbp.route('/users/<int:user_id>/')
class UserHandler(tornado.web.RequestHandler):

    def get(self, user_id):
        self.write("<h3>Hello, user<%d>.<h3>" % int(user_id))
        return self.finish()


if __name__ == '__main__':
    app = tornado.web.Application()
    server = tornado.httpserver.HTTPServer(blueprint.wraps(app))
    server.listen(8000)
    tornado.ioloop.IOLoop.current().start()
