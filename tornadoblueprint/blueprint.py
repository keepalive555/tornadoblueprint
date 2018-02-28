#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tornado Blueprint蓝图的实现。"""

import re
import functools
import threading

import six
from tornado import web


__all__ = ['Blueprint', 'wraps', 'url_for']

__version__ = '0.2.8'
__organization__ = 'www.360.cn'
__author__ = 'gatsby'
__github__ = 'https://github.com/keepalive555/'

_state = threading.local()


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


_REGEXIES = (
    (re.compile(r'<int:.+>'), r'([-+]?\d+)'),  # <int:>
    (re.compile(r'<float:.+>'), r'(\d*\.?\d+)'),  # <float:>
    # 注意：需要用(?:)丢弃捕获到的捕获组，才可以保证捕获到的为完整的uuid
    (re.compile(r'<uuid:.+>'), r'((?:[0-9a-fA-F]+-){4}[0-9a-fA-F]+)'),  # <uuid:>  # noqa
)
_HTTPMETHODS = (
    'GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'HEAD', 'OPTIONS',
)
# XXX: 更优实现，将该方法直接从类的属性里面拿掉？？？
_HANDLERS = [(x, getattr(web.RequestHandler, x.lower())) for x in _HTTPMETHODS]  # noqa


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
        self._errors = set()
        self._error_handler = None

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, v):
        self._enabled = bool(v)

    def _get_handler_name(self, handler):
        return handler.__endpoint__ \
            if hasattr(handler, '__endpoint__') else handler.__class__.__name__

    def errorhandler(self, status_code):

        def decorator(func):
            @functools.wraps(func)
            def wrapper(inst_self, status_code, **kwargs):
                if status_code not in self._errors:
                    return inst_self.__old_error_handler(status_code, **kwargs)
                return func(inst_self, status_code, **kwargs)
            self._errors.add(status_code)
            self._error_handler = wrapper
            return wrapper
        return decorator

    def _add_error_handler(self, handler):
        if self._error_handler:
            handler.__old_error_handler = handler.write_error
            handler.write_error = self._error_handler

    def route(self, uri, params=None, name=None, methods=('GET',)):
        def decorator(handler):
            assert uri[0] == '/'
            internal_uri = uri
            for _re, repl in _REGEXIES:
                internal_uri = _re.sub(repl, internal_uri)
            for method, _handler in _HANDLERS:
                if method in methods:
                    continue
                setattr(handler, method.lower(), _handler)
            self._add_error_handler(handler)
            rule_name = name or '%s.%s' % (
                self.name, self._get_handler_name(handler))
            self.rules.append((self.prefix + internal_uri, handler, params, rule_name))  # noqa: E501

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
    if hasattr(_state, '__app__'):
        return getattr(_state, '__app__')
    assert hasattr(app, 'add_handlers') \
        and hasattr(app.add_handlers, '__call__')
    for host, rules in BlueprintMeta.get_plugged_in_routes():
        app.add_handlers(host, rules)
    setattr(_state, '__app__', app)
    return app


def url_for(endpoint):
    return _state.__app__.reverse_url(endpoint)
