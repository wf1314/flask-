# -*- coding:utf-8 -*-

from datetime import datetime
from ihome import db

class BaseModel(object):
    """模型基类，为每个模型补充创建时间与更新时间"""

    create_time = db.Column(db.DateTime, default=datetime.now)  # 记录的创建时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 记录的更新时间


class User(BaseModel, db.Model):
    """用户"""
    pass
