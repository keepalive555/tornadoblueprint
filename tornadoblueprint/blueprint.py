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
    def get_all_blueprints(self):
        blueprints = []
        for _class in self.derived_class:
            blueprints.extend(_class.blueprints)
        return blueprints


class Blueprint(object):

    __metaclass__ = BlueprintMeta
    blueprints = []

    def __init__(self, host, prefix):
        assert prefix and prefix[0] == '/'
        self.host = host
        self.prefix = prefix
        self.blueprints.append(self)
        self.rules = []

    def route(self, uri):
        def decorator(handler):
            self.rules.append((self.prefix + uri, handler))

            @functools.wraps(handler)
            def wrapper(*args, **kwargs):
                res = handler(*args, **kwargs)
                return res
            return wrapper
        return decorator


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
