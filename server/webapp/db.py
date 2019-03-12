# -*- coding:utf-8 -*-

import shelve

class ShelveProxy(object):
    '''shelve代理
    '''
    def __init__(self, db_name):
        self._db = shelve.open(db_name)
        self._db_name = db_name

    def __getattr__(self, name):
        return getattr(self._db, name)

    def save_status(self, timestamp, status):
        status["timestamp"] = timestamp
        self._db["status"] = status
        # self._db.sync()
        self._db.close()
        self._db = shelve.open(self._db_name)

    def get_status(self):
        return self._db.get("status")

    def save_delta_status(self, last_timestamp, timestamp, delta_status):
        for key in delta_status:
            if key == "timestamp":
                continue
            q = self._db.get(key, [])
            q.append([last_timestamp, timestamp, delta_status.get(key)])
            self._db[key] = q