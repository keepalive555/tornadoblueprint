# TornadoBlueprint

![build](https://travis-ci.org/keepalive555/tornadoblueprint.svg?branch=master)
[![Coverage Status](https://coveralls.io/repos/github/keepalive555/tornadoblueprint/badge.svg?branch=master)](https://coveralls.io/github/keepalive555/tornadoblueprint?branch=master)

## 前言

非常感谢提交`PR`的朋友：[@lichao0x7cc](https://github.com/lichao0x7cc/)。

## 概述

笔者比较喜欢`Flask`框架`route`风格的`URL`路由，`Tornado`框架中`URL`路由是指定`tornado.web.Application`的参数，很不`Pythonic`，所以笔者为`Tornado`框架编写了`Flask`风格蓝图小玩具。

现阶段支持的功能：

- 支持`Blueprint`的`prefix`参数。
- 支持`Blueprint.route`方法的`methods`参数，限定客户端`HTTP Methods`。
- 支持`Blueprint.errorhandler`方法，指定蓝图的错误处理方法（用户可在`tornado.web.RequestHandler`派生与该装饰器之间权衡）。
- 支持`/<int:id>/, <float:id>, <uuid:uuid>`等`Flask`风格的`URI`，兼容`Tornado`正则表达式风格`URL`。
- 支持`Flask`框架的`url_for`函数，使用`RequestHandler`的`__endpoint__`属性指定`endpoint`名称，未指定则默认为`__class__.__name__`。

## 1. 安装

***注意：*** `TornadoBlueprint`已上传至`Python`官方`PYPI`服务器，可通过`pip`命令直接安装，当前最新版本为`0.2.8`。

```bash
pip install tornadoblueprint==0.2.8
```

## 2. 使用

***注意：*** `TornadoBlueprint`示例代码如[demo.py](https://github.com/keepalive555/tornadoblueprint/blob/master/demo.py)所示。
