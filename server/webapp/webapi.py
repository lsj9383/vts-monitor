# -*- coding:utf-8 -*-

from flask import Blueprint, current_app, jsonify, request
from webapp.proto import EnumErrorCode

blue_print = Blueprint('webapi', __name__)

# 测试运行状态
@blue_print.route('/debug')
def test_running():
    return jsonify({ "error_code" : EnumErrorCode.SUCCESS })
