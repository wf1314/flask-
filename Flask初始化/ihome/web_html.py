# -*- coding:utf-8 -*-

# 该模块专门处理静态资源的访问

from flask import Blueprint, current_app, make_response
from flask_wtf.csrf import generate_csrf

web_html = Blueprint('html', __name__)

'''
127.0.0.1:5000/ ---> index.html
127.0.0.1:5000/index.html --> index.html

# 127.0.0.1:5000/favicon.ico  --> 浏览器会主动访问, 获取图标. 会有缓存, 只会再第一次请求时发出


1. 实现正则路由转换器
2. 使用正则转换器, 实现路由匹配
3. 需要除处理图标的访问
4. 设置csrf_token --> 设置的cookie --> csrf_token?
'''


# 点 是任意字符 * 是取 0 至 无限长度
@web_html.route('/<re(".*"):file_name>')
def web_html_demo(file_name):

    print file_name

    # 1. 没有传  --> index.html
    if not file_name:
        # 表示用户访问的是 `/`
        file_name = "index.html"

    # 2. 传入了, 但不是favicon.ico  --> html/ + file_name
    if file_name != 'favicon.ico':
        # 拼接路径
        file_name = "html/" + file_name

    # 3. 传入了favicon.ico

    print '-----'
    print file_name

    # 从wtf.csrf中可以导入generate_csrf.
    # generate_csrf, 会判断session里是否已经有了csrf_token, 如果有, 就返回之前生成的
    # 如果没有, 才会重新生成
    csrf_token = generate_csrf()
    response = make_response(current_app.send_static_file(file_name))
    response.set_cookie('csrf_token', csrf_token)
    return response


# @web_html.route('/')
# def index_demo():
#     return current_app.send_static_file('html/index.html')
#
#
# @web_html.route('/<html>')
# def index_html(html):
#     print html
#
#     # send_static_file: 发送静态文件
#     # 程序运行之后, 再一次请求中, 会产生一个app的代理对象, 这个对象就是current_app
#     # 应用上下文current_app. 此时和app是等价的
#     return current_app.send_static_file('html/index.html')