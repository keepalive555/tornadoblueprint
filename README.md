# TornadoBlueprint

![build](https://travis-ci.org/keepalive555/tornadoblueprint.svg?branch=master)
[![Coverage Status](https://coveralls.io/repos/github/keepalive555/tornadoblueprint/badge.svg?branch=master)](https://coveralls.io/github/keepalive555/tornadoblueprint?branch=master)

> Tornado框架，蓝图功能的第三方轻量级实现，库提供了细粒度接口，可在代码中灵活使用。

## 1. 安装

***注意：*** `TornadoBlueprint`已上传至`Python`官方`PYPI`服务器，可通过`pip`命令直接安装。

```bash
pip install tornadoblueprint
```

## 2. 使用

***注意：*** 首先确认`Tornado`框架已被正确安装。

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
import tornado.ioloop
import tornado.httpserver

from tornadoblueprint.blueprint import Blueprint
from tornadoblueprint.blueprint import HotPlugApplication
from tornadoblueprint.blueprint import get_plugged_in_routes


indexbp = Blueprint(__name__, prefix='/home')


@indexbp.route('/welcome')
class HomeHandler(tornado.web.RequestHandler):

    def get(self):
        self.write("<h3>Hello TornadoBlueprint.<h3>")
        return self.finish()


def get_app1():
    app = tornado.web.Application()
    for host, rules in get_plugged_in_routes():
        app.add_handlers(host, rules)
    return app


def get_app2():
    app = HotPlugApplication()
    app.register_blueprints()
    return app


if __name__ == '__main__':
    app = get_app1()
    server = tornado.httpserver.HTTPServer(app)
    server.listen(8000)
    tornado.ioloop.IOLoop.current().start()

```
