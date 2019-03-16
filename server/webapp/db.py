# -*- coding:utf-8 -*-

import os
import shelve
import fcntl
from webapp.share import LockFile
from webapp.exception import MonitorShelveOpenError

def __open_shelve__(db_name, flag):
    try:
        return shelve.open(db_name, flag=flag)
    except:
        raise MonitorShelveOpenError()

class ShelveProxy(object):
    '''shelve代理
    '''
    def __init__(self, db_home):
        self._db_home = db_home

    def get_count_info(self, date, key):
        db_name = "%s/counter-%s" % (self._db_home, date)
        lock_name = "%s/lock-%s" % (self._db_home, date)
        with LockFile(lock_name, fcntl.LOCK_SH), \
            __open_shelve__(db_name, flag="r") as db:
            # 上文件锁 打开db
            if key:
                return {key : db.get(key, [])}
            dic = {}
            for k in db.keys():
                dic[k] = db[k]
            return dic

    def keys(self, date):
        db_name = "%s/counter-%s" % (self._db_home, date)
        lock_name = "%s/lock-%s" % (self._db_home, date)
        ks = []
        with LockFile(lock_name, fcntl.LOCK_SH), \
            __open_shelve__(db_name, flag="r") as db:
            # 上文件锁 打开db
            for k in db.keys():
                ks.append(k)
        return ks
