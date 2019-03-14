# -*- coding:utf-8 -*-
from __future__ import print_function

import os
import time
import service
import config

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def main():
    timestamp = int(time.time())

    status = service.get_snapshot(config.VTS_STATUS_URL,
                        config.VTS_STATUS_ZONE)
    status["timestamp"] = timestamp
    prev_status = service.get_prev_status(config.SHELVE_DB_VTS_STATUS)
    service.set_status(config.SHELVE_DB_VTS_STATUS, status)

    # 校验上一次的status
    if prev_status is None:
        return "prev status is None, init status"

    prev_timestamp = prev_status.get("timestamp")
    if prev_timestamp is None:
        return "prev timestamp is None, init status again"

    # 计算差异 并入库
    delta_staus = service.compute_delta(prev_status, status)
    service.save_delta_status(config.SHELVE_DB_HOME,
                prev_timestamp,
                timestamp,
                delta_staus)

    return "done"

if __name__ == "__main__":
    print(main())
