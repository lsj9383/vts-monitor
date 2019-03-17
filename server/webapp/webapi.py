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
@blue_print.route('/get')
def count_info():
    today = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    date = request.args.get("date", today)
    key = request.args.get("key")

    db_proxy = current_app.shelve_proxy
    return json.dumps(db_proxy.get_count_info(date, key))

# shelve的获取数据
@blue_print.route('/get/pretty')
def count_info_pretty():
    today = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    date = request.args.get("date", today)
    key = request.args.get("key")

    db_proxy = current_app.shelve_proxy
    return json.dumps(db_proxy.get_count_info_pretty(date, key))


# shelve的获取keys
@blue_print.route('/keys')
def shelve_keys():
    today = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    date = request.args.get("date", today)
    db_proxy = current_app.shelve_proxy
    return json.dumps(db_proxy.keys(date))
