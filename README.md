# TornadoBlueprint

![build](https://travis-ci.org/keepalive555/tornadoblueprint.svg?branch=master)
[![Coverage Status](https://coveralls.io/repos/github/keepalive555/tornadoblueprint/badge.svg?branch=master)](https://coveralls.io/github/keepalive555/tornadoblueprint?branch=master)

## 前言

非常感谢提交`PR`的朋友。

## 概述

笔者比较喜欢`Flask`框架`route`风格的`URL`路由，`Tornado`框架中`URL`路由是指定`tornado.web.Application`的参数，很不`Pythonic`，所以笔者为`Tornado`框架编写了`Flask`风格蓝图小玩具。

现阶段支持的功能：

- 支持`Blueprint`的`prefix`参数。
- 支持`Blueprint.route`方法的`methods`参数，限定客户端`HTTP Methods`。
- 支持`/<int:id>/, <float:id>, <uuid:uuid>`等`Flask`风格的`URI`，兼容`Tornado`正则表达式风格`URL`。

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


@indexbp.route('/shows/<int:_id>/', methods=('GET', 'POST',))
class IntHandler(tornado.web.RequestHandler):

    def get(self, _id):
        self.write("Id is: %d<br>" % int(_id))
        return self.finish()


@indexbp.route('/shows/<float:f1>/<float:f2>/', methods=('GET', 'POST',))
class FloatHandler(tornado.web.RequestHandler):

    def get(self, f1, f2):
        self.write("Sum of %.2f + %.2f = %.2f<br>" % (
            float(f1), float(f2), float(f1)+float(f2)))
        return self.finish()


@indexbp.route('/shows/<uuid:guid>/', methods=('GET', 'POST',))
class UuidHandler(tornado.web.RequestHandler):

    def get(self, guid):
        self.write("Uuid is: %s<br>" % guid)
        return self.finish()


if __name__ == '__main__':
    app = tornado.web.Application()
    server = tornado.httpserver.HTTPServer(blueprint.wraps(app))
    server.listen(8000)
    tornado.ioloop.IOLoop.current().start()
```
