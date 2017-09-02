#!/usr/bin/env python
# -*- coding: utf-8 -*_

from __future__ import print_function

import nose
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.httpclient

from tornadoblueprint.blueprint import (
    Blueprint, BlueprintMeta, HotPlugApplication)


blueprint = Blueprint(__name__, '/home')


@blueprint.route('/welcome')
class DemoHandler(tornado.web.RequestHandler):
    def get(self):
        return self.write('Welcome!')


def test_get_plugged_in_blueprints():
    ret = BlueprintMeta.get_plugged_in_blueprints()
    nose.tools.assert_not_equals(ret, [])


def test_get_plugged_in_routes():
    ret = BlueprintMeta.get_plugged_in_routes()
    nose.tools.assert_not_equals(ret, [])


def test_application():

    def exit_callback():
        client = tornado.httpclient.AsyncHTTPClient()
        ret = client.fetch('http://localhost:8000/home/welcome')
        nose.tools.assert_is_not_none(ret)
        tornado.ioloop.IOLoop.current().stop()

    app = HotPlugApplication()
    app.register_blueprints()
    httpserver = tornado.httpserver.HTTPServer(app)
    httpserver.listen(8000)
    ioloop = tornado.ioloop.IOLoop.current()
    ioloop.add_timeout(ioloop.time() + 1, exit_callback)
    ioloop.start()


if __name__ == '__main__':
    nose.run()
