#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
import tornado.ioloop
import tornado.httpserver

from tornadoblueprint import blueprint


indexbp = blueprint.Blueprint(__name__, prefix='')


@indexbp.route('/shows/<int:_id>/', methods=('GET', 'POST',))
class IntHandler(tornado.web.RequestHandler):

    def get(self, _id):
        self.write("Id is: %d<br>" % int(_id))
        return self.finish()


@indexbp.route('/shows/<float:f1>/<float:f2>/', methods=('GET', 'POST',))
class FloatHandler(tornado.web.RequestHandler):

    def get(self, f1, f2):
        self.write("Sum of %.2f + %.2f = %.2f<br>" % (
            float(f1), float(f2), float(f1) + float(f2)))
        return self.finish()


@indexbp.route('/shows/<uuid:guid>/', methods=('GET', 'POST',))
class UuidHandler(tornado.web.RequestHandler):

    def get(self, guid):
        self.write("Uuid is: %s<br>" % guid)
        return self.finish()


if __name__ == '__main__':
    app = tornado.web.Application()
    server = tornado.httpserver.HTTPServer(blueprint.wraps(app))
    server.listen(8000)
    tornado.ioloop.IOLoop.current().start()
