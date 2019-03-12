# -*- coding:utf-8 -*-

from flask import jsonify
from webapp.proto import EnumErrorCode

class Result(object):
    '''flask结果封装
    '''
    @staticmethod
    def success():
        return jsonify({ "error_code" : EnumErrorCode.SUCCESS })

    @staticmethod
    def error(error_code=EnumErrorCode.BadRequest):
        return jsonify({ "error_code" : error_code })

def compute_delta(last_status, status):
    full_keys = list(last_status.keys())
    full_keys.extend(list(status.keys()))
    full_keys = set(full_keys)

    delta_status = {}
    for key in full_keys:
        if key == "timestamp":
            continue
        pre = last_status.get(key)
        now = status.get(key)
        # 不存在key时取0
        pre_value = pre.get("requestCounter", 0) if pre else 0
        now_value = now.get("requestCounter", 0) if now else 0
        # 值为负数时, 取上一次的delta值作为当前的delta值
        delta_status[key] = now_value - pre_value
    return delta_status