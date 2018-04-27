#! /usr/bin/env python
# -*- coding: utf-8 -*-
import time
import base64
from flask import current_app
from blockmeta import flags, constant
from blockmeta.db import base
from blockmeta.tools.bytom import *
# from blockmeta.tools import util

FLAGS = flags.FLAGS


class BuiltinDriver(base.Base):

    @property
    def type(self):
        return 'builtin'

    def __init__(self):
        self.logger = current_app.logger
        self.mongo_cli = current_app.mongodb_btm
        super(BuiltinDriver, self).__init__()

    # chain default bitcoin
    def request_tx_info(self, tx_hash, detail, chain_id=1):

        try:
            self.mongo_cli.use_db(FLAGS.mongo_bytom)

            dbhash = hashin_hex(tx_hash)
            tx_info = {}
            tx = self.db.get_tx_by_hash(dbhash)
            if tx is None:
                raise Exception("Transcation not found")

            tx_id = tx.get(FLAGS.tx_id)
            tx_version = tx.get(FLAGS.tx_id)
            block_height = tx.get(FLAGS.block_height)

            tx_info['tx_id'] = tx_id
            tx_info['version'] = tx_version
            tx_info['block_height'] = block_height

            return tx_info
        except Exception, e:
            self.logger.error("tx.driver.builtin  Error: %s" % str(e))
            raise Exception(e)

    #
    # def get_coindd(self, tx_id, ntime):
    #     res = self.db.tx_get_coindd(tx_id)
    #     coindd = 0
    #     for r in res:
    #         coindd += (ntime - int(r[0])) * int(r[1]) / 1.0 / 10 ** 8 / 86400
    #     coindd = round(coindd, 2) if coindd > 0 else 0
    #     return coindd
    #
    # def get_addr_map(self, addrs):
    #     addr_map = {}
    #     for addr in addrs:
    #         addr_info = self.mongo_cli.get(table=FLAGS.btc_archives, cond={'address': addr, 'verified': 1})
    #         if addr_info:
    #             addr_map[addr] = {'tag': addr_info['tag'], 'link': addr_info['link']}
    #     return addr_map
    #
    # def get_tx_priority(self, tx_info):
    #     inputs = tx_info['inputs']
    #     bheight = self.db.block_get_latest(1)[0][2]
    #     total = 0
    #     for input in inputs:
    #         amount, prev_hash = float(input['amount']), input['prev_output']
    #         total += amount * constant.BTC_IN_SATOSHIS * self.db.get_confirmations(hashin_hex(input['prev_output']),
    #                                                                                bheight)
    #
    #     if total / int(tx_info['size']) >= constant.PRIORITY_THRESHOLD:
    #         return 1
    #     else:
    #         return 0
    #
    # def _get_tx_time(self, tx_id):
    #     tx_info = self.mongo_cli.get(table=FLAGS.btc_tx_value, cond={'tx_id': int(tx_id)})
    #     return tx_info.get('time', None) if tx_info else None
