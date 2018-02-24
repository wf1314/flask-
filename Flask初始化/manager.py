# -*- coding:utf-8 -*-

# manager.py文件, 只负责程序的启动和命令的添加
# 应该有manager来完全负责程序的启动, 包括是开发模式还是调试模块
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from ihome import create_app
# from ihome import app, db

# 调用创建函数, 获取app和db对象
app, db = create_app('develop')

# 创建命令行的manager
manager = Manager(app)

# 创建迁移对象, 绑定app和db
Migrate(app, db)

# 给命令行对象添加数据库迁移指令
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    # 使用manager运行
    manager.run()
