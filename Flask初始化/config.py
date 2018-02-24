# -*- coding:utf-8 -*-

import redis


# config.py实现配置信息. 使用类与继承的方式实现
class Config(object):
    # 数据库
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1/ihome21'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # secret_key --> 设置session, CSRF
    # import os
    # import base64
    # base64.b64encode(os.urandom(32))
    SECRET_KEY = 'x65Wn0kU2gt+sS6mgKcK/YtQcYrweUna15kVb7cmo08='

    # SECREK_KEY, redis, Session

    # 配置redis的数据
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379

    # 配置session存储到redis中
    PERMANENT_SESSION_LIFETIME = 86400  # 单位是秒, 设置session过期的时间
    SESSION_TYPE = 'redis'  # 指定存储session的类型为redis
    SESSION_USE_SIGNER = True  # 对数据进行签名加密, 提高安全性
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)  # 设置redis的ip和端口



class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    # SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@119.203.123.1/ihome21'
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    pass


config_dict = {
    'develop':  DevelopmentConfig,
    'production': ProductionConfig
}
