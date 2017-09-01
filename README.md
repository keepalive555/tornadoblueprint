# TornadBlueprint

![build](https://travis-ci.org/keepalive555/tornadoblueprint.svg?branch=master)

> Tornado框架，蓝图功能的第三方实现。

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


indexbp = Blueprint(__name__, prefix='/home')
indexbp.hotplug = True  # try False.


@indexbp.route('/welcome')
class IndexHanlder(tornado.web.RequestHandler):

    def get(self):
        return self.write("Hello TornadoBlueprint.")


if __name__ == '__main__':
    app = HotPlugApplication()
    app.register_blueprints()
    server = tornado.httpserver.HTTPServer(app)
    server.listen(8000)
    tornado.ioloop.IOLoop.current().start()

```