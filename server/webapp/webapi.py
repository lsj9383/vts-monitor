# -*- coding:utf-8 -*-

import time
import json
import requests

from flask import Blueprint, current_app, request
from webapp.proto import EnumErrorCode
from webapp.share import Result

blue_print = Blueprint('webapi', __name__)

# 测试运行状态
@blue_print.route('/debug')
def test_running():
    return Result.success()

# shelve的获取数据
@blue_print.route('/db_get')
def shelve_value():
    pass

# shelve的获取keys
@blue_print.route('/db_keys')
def shelve_keys():
    pass
