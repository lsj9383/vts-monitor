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
