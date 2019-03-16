# -*- coding:utf-8 -*-

import time
import json
from flask import jsonify, request, session, g, current_app, render_template
from webapp import exception
from webapp.share import Result, Watcher

__ok_request_status__ = 200

def register(app):
    @app.before_request
    def preprocess():
        g.watcher = Watcher()

    @app.after_request
    def after_process(rv):
        message = "req : %s, cost : %s ms" % (request.url, g.watcher.delayed())
        current_app.logger.info(message)
        return rv

    @app.errorhandler(exception.MonitorException)
    def exception_handler(e):
        message = str(e)
        status = __ok_request_status__
        error_result = (e.error_code(), message)
        return (Result.error(e.error_code(), message), status)
