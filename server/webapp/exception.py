# -*- coding:utf-8 -*-

class MonitorException(Exception):
    def __init__(self, value):
        super().__init__(value)

    def error_code(self):
        return error_code_mapper.get(type(self), 90000)

class MonitorBadRequest(MonitorException):
    def __init__(self):
        super().__init__("请求失败")

class MonitorInvalidRequest(MonitorException):
    def __init__(self):
        super().__init__("请求参数错误")

class MonitorInternalError(MonitorException):
    def __init__(self):
        super().__init__("服务器错误")

class MonitorShelveOpenError(MonitorException):
    def __init__(self):
        super().__init__("打开数据库失败, 或许数据不存在")

error_code_mapper = {
    MonitorException : 1000,
    MonitorBadRequest : 1001,
    MonitorInvalidRequest : 1002,
    MonitorInternalError : 1003,
    MonitorShelveNotExist : 1004,
}