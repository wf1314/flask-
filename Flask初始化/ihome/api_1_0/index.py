# -*- coding:utf-8 -*-

import logging
# TODO(huizhubo) 记得导入models
from ihome import models
from ihome import redis_store
from . import api
from flask import session

from ihome import db # 视图函数中肯定需要用db, 所以不能断
# 2. 使用蓝图对象实现路由


@api.route('/index', methods=['GET', 'POST'])
def index():


    return 'index'


