# -*- coding:utf-8 -*-

import time
import fcntl
import requests
import shelve

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

def get_snapshot(url, zone):
    '''从vts获得当前的状态
    '''
    if url is None or zone is None:
        raise Exception("url or zone is None")

    r = requests.get(url).json()
    zones = r.get("filterZones")
    if zones is None:
        raise Exception("zone is not exist")
    status = zones.get(zone)
    if status is None:
        raise Exception("status is None")
    return status

def get_prev_status(db_name):
    '''获得上一级状态
    '''
    with shelve.open(db_name) as db:
        prev_status = db.get("status")
        return prev_status

def set_status(db_name, status):
    '''设置当前状态
    '''
    with shelve.open(db_name) as db:
        db["status"] = status

def compute_delta(prev_status, status):
    '''计算两个状态之间的差值信息
    '''
    full_keys = list(prev_status.keys())
    full_keys.extend(list(status.keys()))
    full_keys = set(full_keys)

    delta_status = {}
    for key in full_keys:
        if key == "timestamp":
            continue
        pre = prev_status.get(key)
        now = status.get(key)
        # 不存在key时取0
        pre_value = pre.get("requestCounter", 0) if pre else 0
        now_value = now.get("requestCounter", 0) if now else 0
        # 值为负数时, 取上一次的delta值作为当前的delta值
        delta_status[key] = now_value - pre_value
    return delta_status
    
def save_delta_status(shelve_home, prev_timestamp, timestamp, delta_status):
    '''记录差异的状态
    '''
    today = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    db_name = "%s/counter-%s" % (shelve_home, today)
    lock_name = "%s/lock-%s" % (shelve_home, today)

    # TODO(arthurlu) 上锁
    with LockFile(lock_name):
        _save_delta_status(db_name, prev_timestamp, timestamp, delta_status)

def _save_delta_status(db_name, prev_timestamp, timestamp, delta_status):
    with shelve.open(db_name) as db:
        for key in delta_status:
            if key == "timestamp":
                continue
            q = db.get(key, [])
            q.append([prev_timestamp, timestamp, delta_status.get(key)])
            db[key] = q