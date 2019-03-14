# -*- coding:utf-8 -*-

import logging

class __BaseConfig__:
    # 服务器基本配置
    DEBUG = True
    PORT = 5000
    STATIC_FOLDER = "../../static"

    # 日志配置
    LOGGER_LEVEL = logging.INFO
    LOGGER_FORMAT = "[%(levelname)s] [%(asctime)s]%(message)s"
    LOGGER_FILE = "./logs/base.log"

    # 本地db配置
    SHELVE_DB_HOME = "../shelve_db/"

base = __BaseConfig__()
