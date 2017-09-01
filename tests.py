#!/usr/bin/env python
# -*- coding: utf-8 -*_

from __future__ import print_function

import nose
import tornado.web
import tornado.ioloop
import tornado.httpserver

from tornadoblueprint.blueprint import (
    Blueprint, BlueprintMeta, HotPlugApplication)


blueprint = Blueprint(__name__, '/users')


@blueprint.route('/list', name='demo')
class DemoHandler(tornado.web.RequestHandler):
    def get(self):
        return self.write('demo handler.')


def setup_func():
    pass


def teardown_func():
    pass


@nose.with_setup(setup_func, teardown_func)
def test_get_plugged_in_blueprints():
    ret = BlueprintMeta.get_plugged_in_blueprints()
    nose.tools.assert_not_equals(ret, [])


@nose.with_setup(setup_func, teardown_func)
def test_get_plugged_in_routes():
    ret = BlueprintMeta.get_plugged_in_routes()
    nose.tools.assert_not_equals(ret, [])


@nose.with_setup(setup_func, teardown_func)
def test_application():

    def exit_callback():
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
