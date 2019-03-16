# -*- coding:utf-8 -*-

import time
import json
from flask import jsonify, request, session, g, current_app, render_template
from webapp import exception
from webapp.share import Result

__ok_request_status__ = 200

def register(app):
    @app.errorhandler(exception.MonitorException)
    def exception_handler(e):
        message = str(e)
        status = __ok_request_status__
        error_result = (e.error_code(), message)
        return (Result.error(e.error_code(), message), status)
