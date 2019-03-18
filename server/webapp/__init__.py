# -*- coding:utf-8 -*-

import os
import logging
from flask_session import Session
from flask import Flask, g, Response
from webapp import webapi, db, hook

def create_app(configure):
    # 创建服务器
    app = Flask(__name__, static_folder=configure.STATIC_FOLDER)

    # 导入配置对象
    app.config.from_object(configure)

    # 配置shelve数据库
    app.shelve_proxy = db.ShelveProxy(configure.SHELVE_DB_HOME)

    # 日志系统
    if not os.path.exists(os.path.dirname(configure.LOGGER_FILE)):
        os.mkdir(os.path.dirname(configure.LOGGER_FILE))
    file_handler = logging.FileHandler(configure.LOGGER_FILE, encoding='UTF-8')
    file_handler.setLevel(configure.LOGGER_LEVEL)
    file_handler.setFormatter(logging.Formatter(configure.LOGGER_FORMAT))
    app.logger.setLevel(configure.LOGGER_LEVEL)
    app.logger.addHandler(file_handler)

    # 注册蓝图
    app.register_blueprint(webapi.blue_print, url_prefix='/monitor')

    # 注册钩子
    hook.register(app)

    return app
