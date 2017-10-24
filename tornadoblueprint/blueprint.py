#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tornado Blueprint蓝图的实现。"""

import re
import functools

import six


__all__ = ['Blueprint', 'wraps']


__version__ = '0.2.1'
__organization__ = 'www.360.cn'
__author__ = 'gatsby'
__github__ = 'https://github.com/keepalive555/'


class BlueprintMeta(type):

    derived_class = []

    def __new__(metacls, cls_name, bases, namespace):
        _class = super(BlueprintMeta, metacls).__new__(
            metacls, cls_name, bases, namespace)
        metacls.derived_class.append(_class)
        return _class

    @classmethod
    def get_plugged_in_blueprints(metacls):
        blueprints = []
        for _class in metacls.derived_class:
            blueprints.extend(
                [x for x in _class.blueprints if x.enabled is True])
        return blueprints

    @classmethod
    def get_plugged_in_routes(metacls):
        routes = []
        for blueprint in metacls.get_plugged_in_blueprints():
            routes.append((blueprint.host, blueprint.rules))
        return routes


_REGEXIES = [
    (re.compile(r'<int:.+>'), r'(\d+)'),
]


@six.add_metaclass(BlueprintMeta)
class Blueprint(object):

    blueprints = []

    def __init__(self, name, prefix='', host='.*'):
        self.name = name
        self.host = host
        self.prefix = prefix

        self.blueprints.append(self)
        self.rules = []
        self._enabled = True

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, v):
        self._enabled = bool(v)

    def route(self, uri, params=None, name=None, methods=None):
        def decorator(handler):
            assert uri[0] == '/'
            internal_uri = uri
            for _re, repl in _REGEXIES:
                internal_uri = _re.sub(repl, internal_uri)
            self.rules.append((self.prefix + internal_uri, handler, params, name))  # noqa: E501

            @functools.wraps(handler)
            def wrapper(*args, **kwargs):
                res = handler(*args, **kwargs)
                return res
            return wrapper
        return decorator

    def __call__(self, *args, **kwargs):
        return self.route(*args, **kwargs)

    def get_route_rules(self):
        return self.host, self.rules


def wraps(app):
    assert hasattr(app, 'add_handlers') \
        and hasattr(app.add_handlers, '__call__')
    for host, rules in BlueprintMeta.get_plugged_in_routes():
        app.add_handlers(host, rules)
    return app
