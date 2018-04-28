#! /usr/bin/env python
# -*- coding: utf-8 -*-

# from flask import current_app
from flask.ext.restful import Resource

from tools import flags
from blockmeta.tools.bytom import is_hash_prefix
from manager import TxManager
from blockmeta.constant import DEFAULT_OFFSET

FLAGS = flags.FLAGS


class TxAPI(Resource):

    def __init__(self):
        self.manager = TxManager()

    def get(self, tx_hash):
        if not is_hash_prefix(tx_hash):
            raise Exception("Transaction hash is wrong!")

        result = self.manager.handle_tx(tx_hash) if tx_hash else {}
        return result


class TxListAPI(Resource):

    def __init__(self):
        self.manager = TxManager()

    def get(self, num=DEFAULT_OFFSET):
        result = self.manager.list_txs(num)
        return result
