#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tornado Blueprint蓝图的实现。"""

import functools

import tornado.web


__version__ = '1.0.0'
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
    def get_all_blueprints(metacls):
        blueprints = []
        for _class in metacls.derived_class:
            blueprints.extend(_class.blueprints)
        return blueprints

    @classmethod
    def get_all_routes(metacls):
        routes = []
        for blueprint in metacls.get_all_blueprints():
            routes.append((blueprint.host, blueprint.rules))
        return routes


class Blueprint(object):

    __metaclass__ = BlueprintMeta
    blueprints = []

    def __init__(self, name, prefix, host='.*'):
        assert prefix and prefix[0] == '/'
        self.name = name
        self.host = host
        self.prefix = prefix

        self.blueprints.append(self)
        self.rules = []

    def route(self, uri, params=None, name=None):
        def decorator(handler):
            self.rules.append((self.prefix + uri, handler, params, name))

            @functools.wraps(handler)
            def wrapper(*args, **kwargs):
                res = handler(*args, **kwargs)
                return res
            return wrapper
        return decorator

    def get_route_rules(self):
        return self.host, self.rules

    @staticmethod
    def get_blueprint(cls, name):
        for blueprint in cls.blueprints:
            if blueprint.name == name:
                break
        return blueprint


class HotSwapApplication(tornado.web.Application):

    def __init__(self, *args, **kwargs):
        if args and args[0] \
                and isinstance(args[0], tornado.web.Application):
            _inst = args[0]
        else:
            _inst = self
        super(HotSwapApplication, _inst).__init__(*args, **kwargs)

    @classmethod
    def proxy(cls, app):
        return cls(app)

    def register_blueprints(self):
        blueprints = BlueprintMeta.get_all_blueprints()
        for blueprint in blueprints:
            self.add_handlers(blueprint.host, blueprint.rules)
        return blueprints
