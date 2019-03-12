# -*- coding:utf-8 -*-

import time
import json
import requests

from flask import Blueprint, current_app, request
from webapp.proto import EnumErrorCode, MAX_COUNT_VALUE
from webapp.share import Result, compute_delta

blue_print = Blueprint('webapi', __name__)

# 测试运行状态
@blue_print.route('/debug')
def test_running():
    return Result.success()

# 保存vts状态快照
@blue_print.route('/snapshot')
def status_snapshot():
    timestamp = int(time.time())
    vts_status_url = current_app.config.get("VTS_STATUS_URL")
    vts_status_zone = current_app.config.get("VTS_STATUS_ZONE")

    if vts_status_url is None or vts_status_zone is None:
        return Result.error(EnumErrorCode.InternalServerError)

    response = requests.get(vts_status_url)
    r = response.json()
    zones = r.get("filterZones")
    if zones is None:
        return Result.error()
    status = zones.get(vts_status_zone)
    if status is None:
        return Result.error()
    last_status = current_app.shelve_proxy.get_status()
    current_app.shelve_proxy.save_status(timestamp, status)
    # (TODO)lu 比较当前status和上一级的status，计算增量
    if last_status is None:
        return Result.success()
    last_timestamp = last_status.get("timestamp")
    delta_staus = compute_delta(last_status, status)
    current_app.shelve_proxy.save_delta_status(
                                last_timestamp,
                                timestamp,
                                delta_staus)
    return Result.success()

# shelve的获取数据
@blue_print.route('/db_get')
def shelve_value():
    key = request.args.get("key")
    if key is None:
        return Result.error()
    s = current_app.shelve_proxy.get(key)
    return json.dumps(s)

# shelve的获取keys
@blue_print.route('/db_keys')
def shelve_keys():
    keys = []
    for key in current_app.shelve_proxy.keys():
        keys.append(key)
    return json.dumps(keys)
