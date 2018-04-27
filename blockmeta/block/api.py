#! /usr/bin/env python
# -*- coding: utf-8 -*-

# from flask import current_app
from flask.ext.restful import Resource

from tools import flags
from manager import BlockManager

FLAGS = flags.FLAGS


class BlockAPI(Resource):

    def __init__(self):
        self.manager = TxManager()

    def get(self, tx_hash):
        result = self.manager.handle_tx(tx_hash) if tx_hash else {}
        return result


class TxListAPI(Resource):

    def __init__(self):
        self.manager = TxManager()

    def get(self, num):
        result = self.manager.list_txs(num)
        return result
