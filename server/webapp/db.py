# -*- coding:utf-8 -*-

import shelve

def shelve_open(db_name):
    return shelve.open(db_name)

def shelve_close(shelve_db):
    shelve_db.close()