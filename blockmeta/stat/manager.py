# -*- coding: utf-8 -*-

from flask import current_app
from driver.builtin import BuiltinDriver


class StatManager:

    def __init__(self):
        self.driver = BuiltinDriver()
        self.logger = current_app.logger

    def handle_stat(self):
        try:
            return self.driver.request_stat_info()
        except Exception, e:
            self.logger.error("StatManager.handle_stat Error: %s" % str(e))
            raise Exception("handle_stat error: %s", e)
