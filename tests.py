#!/usr/bin/env python
# -*- coding: utf-8 -*_

from __future__ import print_function

import nose
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.httpclient

from tornadoblueprint import blueprint


bp = blueprint.Blueprint(__name__, '/home')


@bp.route('/welcome')
class DemoHandler(tornado.web.RequestHandler):
    def get(self):
        return self.write('Welcome!')


def test_wraps():

    def exit_callback():
        client = tornado.httpclient.AsyncHTTPClient()
        ret = client.fetch('http://localhost:8000/home/welcome')
        nose.tools.assert_is_not_none(ret)
        tornado.ioloop.IOLoop.current().stop()

    httpserver = tornado.httpserver.HTTPServer(
        blueprint.wraps(tornado.web.Application()))
    httpserver.listen(8000)
    ioloop = tornado.ioloop.IOLoop.current()
    ioloop.add_timeout(ioloop.time() + 1, exit_callback)
    ioloop.start()


if __name__ == '__main__':
    nose.run()
