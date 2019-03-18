# -*- coding:utf-8 -*-

import time
import json
import requests

from flask import Blueprint, current_app, request
from webapp.proto import EnumErrorCode
from webapp.share import Result, local_cache

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
    return _get_count_info(date, key)
    

# shelve的获取数据
@blue_print.route('/get/pretty')
def count_info_pretty():
    today = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    date = request.args.get("date", today)
    key = request.args.get("key")
    return _get_count_info_pretty(date, key)

# shelve的获取keys
@blue_print.route('/keys')
def shelve_keys():
    today = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    date = request.args.get("date", today)
    return _get_keys(date)

# 获取所有的时间
@blue_print.route('/dates')
def shelve_dates():
    db_proxy = current_app.shelve_proxy
    return json.dumps(db_proxy.dates())

@local_cache()
def _get_count_info(date, key):
    db_proxy = current_app.shelve_proxy
    return json.dumps(db_proxy.get_count_info(date, key))

@local_cache()
def _get_count_info_pretty(date, key):
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

@local_cache()
def _get_keys(date):
    db_proxy = current_app.shelve_proxy
    return json.dumps(db_proxy.keys(date))
