#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import current_app
from flask.ext.restful import Resource

from tools import flags
from blockmeta.tools.bytom import is_hash_prefix
from manager import TxManager

FLAGS = flags.FLAGS


class TxAPI(Resource):

    def __init__(self):
        self.manager = TxManager()
        self.logger = current_app.logger

    def get(self, tx_hash):
        result = self.manager.handle_tx(tx_hash) if tx_hash else {}
        return result
