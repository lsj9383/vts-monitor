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
def shelve_value():
    today = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    date = request.args.get("date", today)
    key = request.args.get("key")

    db_proxy = current_app.shelve_proxy
    return json.dumps(db_proxy.get_count_info(date, key))

# shelve的获取数据
@blue_print.route('/get/pretty')
def shelve_value():
    today = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    date = request.args.get("date", today)
    key = request.args.get("key")

    db_proxy = current_app.shelve_proxy
    count_infos = db_proxy.get_count_info(date, key)
    for k, v in count_infos.items():
        for item in v:
            if len(item) != 3:
                continue
            start = time.strftime('%H:%M:%S',time.localtime(item[0]))
            end = time.strftime('%H:%M:%S',time.localtime(item[1]))
            item[0] = start
            item[1] = end
    return json.dumps(count_infos)


# shelve的获取keys
@blue_print.route('/keys')
def shelve_keys():
    db_proxy = current_app.shelve_proxy
    return db_proxy.keys()
