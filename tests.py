#!/usr/bin/env python
# -*- coding: utf-8 -*_

from __future__ import print_function

import nose
import tornado.web

from tornadoblueprint.blueprint import Blueprint


def setup_func():
    pass


def teardown_func():
    pass


@nose.with_setup(setup_func, teardown_func)
def test_blueprint():
    blueprint = Blueprint('*.example.com', '/users')

    @blueprint.route('/list')
    class DemoHandler(tornado.web.RequestHandler):

        def get(self):
            self.write('demo handler.')


if __name__ == '__main__':
    nose.run()
