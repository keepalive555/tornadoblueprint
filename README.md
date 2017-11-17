# TornadoBlueprint

![build](https://travis-ci.org/keepalive555/tornadoblueprint.svg?branch=master)
[![Coverage Status](https://coveralls.io/repos/github/keepalive555/tornadoblueprint/badge.svg?branch=master)](https://coveralls.io/github/keepalive555/tornadoblueprint?branch=master)

## 概述

笔者比较喜欢`Flask`框架`route`风格的`URL`路由，`Tornado`框架中`URL`路由是指定`tornado.web.Application`的参数，很不`Pythonic`，所以笔者为`Tornado`框架编写了`Flask`风格蓝图小玩具。

现阶段支持的功能：

- 支持`Blueprint`的`prefix`参数。
- 支持`Blueprint.route`方法的`methods`参数，限定客户端`HTTP Methods`。
- 支持`/<int:id>/`等`Flask`风格的`URI`，兼容`Tornado`正则表达式风格`URL`。

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


@indexbp.route('/users/<int:user_id>/plans/<int:plan_id>')
class UserHandler(tornado.web.RequestHandler):

    def get(self, user_id, plan_id):
        self.write("<h3>Hello, user<%d> plan<%d>.<h3>" % (int(user_id), int(plan_id)))
        return self.finish()


if __name__ == '__main__':
    app = tornado.web.Application()
    server = tornado.httpserver.HTTPServer(blueprint.wraps(app))
    server.listen(8000)
    tornado.ioloop.IOLoop.current().start()

```
