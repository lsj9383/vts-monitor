# -*- coding:utf-8 -*-

import fcntl
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

class LockFile:
    '''文件锁
    '''
    def __init__(self, lock_name, lock_type=fcntl.LOCK_EX):
        self._lock_name = lock_name
        self._lock_type = lock_type

    def __enter__(self):
        self._flock = open(self._lock_name, 'w')
        fcntl.flock(self._flock , self._lock_type)
        return self

    def __exit__(self, type, value, traceback):
        fcntl.flock(self._flock, fcntl.LOCK_UN)
        self._flock.close()
