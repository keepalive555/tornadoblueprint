#!/usr/bin/env python
# -*- coding: utf-8 -*_

from __future__ import print_function

import nose
import tornado.web
import tornado.ioloop
import tornado.httpserver

from tornadoblueprint.blueprint import (
    Blueprint, BlueprintMeta,  HotSwapApplication)


blueprint = Blueprint(r'localhost', '/users')


@blueprint.route('/list')
class DemoHandler(tornado.web.RequestHandler):
    def get(self):
        return self.write('demo handler.')


def setup_func():
    pass


def teardown_func():
    pass


@nose.with_setup(setup_func, teardown_func)
def test_get_all_blueprints():
    ret = BlueprintMeta.get_all_blueprints()
    nose.tools.assert_not_equals(ret, [])
    print(ret)


@nose.with_setup(setup_func, teardown_func)
def test_application():

    def exit_callback():
        print("quit ioloop.")
        tornado.ioloop.IOLoop.current().stop()

    app = HotSwapApplication()
    print(app.register_blueprints())
    httpserver = tornado.httpserver.HTTPServer(app)
    httpserver.listen(8000)
    ioloop = tornado.ioloop.IOLoop.current()
    ioloop.add_timeout(ioloop.time() + 1, exit_callback)
    ioloop.start()


if __name__ == '__main__':
    nose.run()
