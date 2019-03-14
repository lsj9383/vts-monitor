# -*- coding:utf-8 -*-

import os
import shelve
import fcntl
from webapp.share import LockFile

class ShelveProxy(object):
    '''shelve代理
    '''
    def __init__(self, db_home):
        self._db_home = db_home

    def get_count_info(self, date, key):
        db_name = "%s/counter-%s" % (self._db_home, date)
        lock_name = "%s/lock-%s" % (self._db_home, date)
        # 上文件锁
        with LockFile(lock_name, fcntl.LOCK_SH):
            with shelve.open(db_name, flag="r") as db:
                if key:
                    return {key : db.get(key)}
                dic = {}
                for k in db.keys():
                    dic[k] = db[k]
                return dic
