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

from tornadoblueprint import blueprint


indexbp = blueprint.Blueprint(__name__, prefix='')


@indexbp.route('/users/<int:user_id>/')
class UserHandler(tornado.web.RequestHandler):

    def get(self, user_id):
        self.write("<h3>Hello, user<%d>.<h3>" % int(user_id))
        return self.finish()


if __name__ == '__main__':
    app = tornado.web.Application()
    server = tornado.httpserver.HTTPServer(blueprint.wraps(app))
    server.listen(8000)
    tornado.ioloop.IOLoop.current().start()

```
