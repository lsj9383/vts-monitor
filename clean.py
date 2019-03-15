#!/usr/bin/python
# -*- coding:utf-8 -*-

import os

name_list = ("__pycache__", "lock*", "counter*.db", "vts-status.db")

for name in name_list:
    os.system("find ./ -name '{0}' | xargs rm -rf".format(name))
