# -*- coding: utf-8 -*-

from flask_restful import Resource, reqparse

from manager import StatManager
from tools import flags

FLAGS = flags.FLAGS


class StatAPI(Resource):

    def __init__(self):
        self.manager = StatManager()

    def get(self):
        return self.manager.handle_stat

