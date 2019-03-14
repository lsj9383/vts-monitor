# -*- coding:utf-8 -*-

import shelve

class ShelveProxy(object):
    '''shelve代理
    '''
    def __init__(self, db_home):
        self._db_home = db_home