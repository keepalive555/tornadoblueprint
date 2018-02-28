#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
import tornado.ioloop
import tornado.httpserver

from tornadoblueprint import blueprint


indexbp = blueprint.Blueprint('index', prefix='')


@indexbp.errorhandler(500)
def internal_error(self, status_code, **kwargs):
    return self.finish("error!")


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


@indexbp.route('/index', methods=('GET', ))
class IndexHandler(tornado.web.RequestHandler):

    __endpoint__ = 'index'

    def get(self):
        self.write('Index!!!')
        return self.finish()


@indexbp.route('/shows/<uuid:guid>/', methods=('GET', 'POST',))
class UuidHandler(tornado.web.RequestHandler):

    def get(self, guid):
        self.write("Uuid is: %s<br>" % guid)
        return self.redirect(blueprint.url_for('index.index'))


@indexbp.route('/shows/error', methods=('GET',))
class ErrorHandler(tornado.web.RequestHandler):

    def get(self):
        a = 100
        b = 0
        a / b

    def write_error(self, status_code, **kwargs):
        self.finish("lalalala")


if __name__ == '__main__':
    app = tornado.web.Application()
    server = tornado.httpserver.HTTPServer(blueprint.wraps(app))
    server.listen(8000)
    tornado.ioloop.IOLoop.current().start()
