#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1.0
@author: CJ
@software: PyCharm
@file: cmdline.py
@time: 2017/11/5 0:42
"""

from scrapy import cmdline

cmdline.execute("scrapy crawl hanfu".split())
