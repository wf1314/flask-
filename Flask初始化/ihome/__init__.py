# -*- coding:utf-8 -*-

import redis
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config_dict, Config
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from logging.handlers import RotatingFileHandler
from ihome.utils.commons import RegexConverter

# 目前, db的创建, 放入了函数中. 其他文件用的的时候, 希望直接获取db
db = SQLAlchemy()


# 外界将来需要用到redis来做存储或读取. redis的创建应该放在和app创建一样的文件中. 留出对象供外界调用
redis_store = None

'''
定义一个函数, 接受参数, 返回app和db:
封装函数会遇到的两件事: 
1. db创建的时机问题: 外面要用, 但是前面不能导入app, 需要在app之后才能init
2. db如果被视图函数导入, 此时会发生循环引用的问题, 将蓝图的导入延迟
'''

'''
CSRF保护
POST,DELETE,PUT在表单提交时, 对需要开启保护
'''

'''
日志等级
ERROR 错误级别
WARN  警告级别
INFO  信息级别
DEBUG 调试级别

在实际开发中, 可以用日志来替代print. 后续就可以通过级别的设置, 来控制log的输出
一般用于查看信息的print, 可以不用注释或删除, 直接更改更高的级别, 就不会输出了. 以便发布时使用
'''

# 设置日志的记录等级
logging.basicConfig(level=logging.DEBUG)  # 调试debug级
# 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024*1024*100, backupCount=10)
# 创建日志记录的格式                 日志等级    输入日志信息的文件名 行数    日志信息
formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
# 为刚创建的日志记录器设置日志记录格式
file_log_handler.setFormatter(formatter)
# 为全局的日志工具对象（flask app使用的）添加日志记录器
logging.getLogger().addHandler(file_log_handler)


# create_app: 创建app, db, csrt, session
def create_app(config_name):
    app = Flask(__name__)

    # 添加自定义的路由转换器
    app.url_map.converters['re'] = RegexConverter

    # 配置需要紧跟着app的创建, 以便于其他对象创建时能够找到对应的参数
    app.config.from_object(config_dict[config_name])

    # 可以延迟导入app对象 --> 用app核心是为了获取配置文件
    db.init_app(app)
    # db = SQLAlchemy(app)

    # CSRF保护
    #'A secret key is required to use CSRF: CSRF需要设置SECRET_KEY
    CSRFProtect(app)

    # 创建redis
    # global: 使用全局的redis_store
    global redis_store
    redis_store = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)

    # Flask-Session扩展, 可以将cookie中的session信息同步到redis中
    Session(app)

    # 为了解决循环导入, 可以将某一方延迟导入(用到时再导入)
    from ihome.api_1_0 import api  # 这里也不能断, 否则没有蓝图对象

    # 注册蓝图对象
    app.register_blueprint(api, url_prefix='/api/v1_0')

    # 在同级目录, 直接导入即可. 不需要from
    import web_html
    app.register_blueprint(web_html.web_html)

    return app, db

