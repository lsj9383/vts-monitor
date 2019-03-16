# -*- coding:utf-8 -*-

import fcntl
import time
from flask import jsonify
from webapp.proto import EnumErrorCode

class Result(object):
    '''flask结果封装
    '''
    @staticmethod
    def success():
        return jsonify({ "error_code" : EnumErrorCode.SUCCESS })

    @staticmethod
    def error(error_code=EnumErrorCode.BadRequest, message=None):
        resp = { "error_code" : error_code }
        if message:
            resp["error_message"] = message
        return jsonify(resp)

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

class Watcher:
    '''请求观察类, 该类用于观察请求的细节:
        * 请求的id
        * 请求的延时
    '''
    def __init__(self):
        self._create = time.time()

    def delayed(self):
        '''输出延时
        '''
        now = time.time()
        return int((now - self._create)*1000)

    def create(self):
        '''当前请求时间戳
        '''
        return self._create

    def ident(self):
        '''请求标识
        '''
        return id(self)
