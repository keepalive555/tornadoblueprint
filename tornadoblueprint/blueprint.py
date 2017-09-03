#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tornado Blueprint蓝图的实现。"""

import functools

import six
import tornado.web


__version__ = '0.1.8'
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
                [x for x in _class.blueprints if x.hotplug is True])
        return blueprints

    @classmethod
    def get_plugged_in_routes(metacls):
        routes = []
        for blueprint in metacls.get_plugged_in_blueprints():
            routes.append((blueprint.host, blueprint.rules))
        return routes


def get_plugged_in_blueprints():
    return BlueprintMeta.get_plugged_in_blueprints()


def get_plugged_in_routes():
    return BlueprintMeta.get_plugged_in_routes()


@six.add_metaclass(BlueprintMeta)
class Blueprint(object):

    blueprints = []

    def __init__(self, name, prefix='', host='.*'):
        self.name = name
        self.host = host
        self.prefix = prefix

        self.blueprints.append(self)
        self.rules = []
        self._hotplug = True

    @property
    def hotplug(self):
        return self._hotplug

    @hotplug.setter
    def hotplug(self, v):
        if isinstance(v, bool):
            self._hotplug = v

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
                return blueprint


class HotPlugApplication(tornado.web.Application):

    def __init__(self, *args, **kwargs):
        if args and args[0] \
                and isinstance(args[0], tornado.web.Application):
            _inst = args[0]
        else:
            _inst = self
        super(HotPlugApplication, _inst).__init__(*args, **kwargs)

    @classmethod
    def proxy(cls, app):
        return cls(app)

    def register_blueprints(self):
        for host, rules in get_plugged_in_routes():
            self.add_handlers(host, rules)
