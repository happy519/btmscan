#! /usr/bin/env python
# -*- coding: utf-8 -*-


from tools import flags, exception
from blockmeta.tools.bytom import *
from blockmeta.db.mongo import MongodbClient
from blockmeta import constant

FLAGS = flags.FLAGS


class BuiltinDriver:
    @property
    def type(self):
        return 'builtin'

    def __init__(self):
        self.mongo_cli = MongodbClient(
            host=FLAGS.mongo_bytom_host,
            port=FLAGS.mongo_bytom_port)
        self.mongo_cli.use_db(FLAGS.mongo_bytom)

    def request_tx_info(self, tx_hash):
        try:
            dbhash = hashin_hex(tx_hash)
            tx_info = {}
            tx = self.get_tx_by_hash(dbhash)
            if tx is None:
                raise Exception("Transaction not found")

            tx_id = tx.get(FLAGS.tx_id)
            tx_version = tx.get(FLAGS.tx_id)
            block_height = tx.get(FLAGS.block_height)
            tx_in = tx.get(FLAGS.transaction_in)
            tx_out = tx.get(FLAGS.transaction_out)
            tx_size = tx.get(FLAGS.size)
            value_in = 0
            value_out = 0

            if len(tx_in) != 0:
                for tx in tx_in:
                    if tx.get(FLAGS.tx_io_type) == "spend" and tx.get(FLAGS.asset_id) == constant.BYTOM_ASSET_ID:
                        value_in += tx.get(FLAGS.amount)

            if len(tx_out) != 0:
                for tx in tx_out:
                    # type can be "retain"
                    if tx.get(FLAGS.tx_io_type) == "control" and tx.get(FLAGS.asset_id) == constant.BYTOM_ASSET_ID:
                        value_out += tx.get(FLAGS.amount)

            tx_fee = value_in - value_out

            tx_info['tx_id'] = tx_id
            tx_info['version'] = tx_version
            tx_info['block_height'] = block_height
            tx_info['value_in'] = value_in
            tx_info['value_out'] = value_out
            tx_info["fee"] = tx_fee
            tx_info["size"] = tx_size
            tx_info['txin'] = tx_in
            tx_info['txout'] = tx_out

            return tx_info
        except Exception, e:
            raise Exception(e)

    def get_tx_list(self, n=1000):
        try:
            txs = self.mongo_cli.get_last_n(table=FLAGS.transaction_info, args=None, order=FLAGS.block_height, n=n)
        except Exception, e:
            raise exception.DBError(e)
        return txs

    def get_tx_by_hash(self, txhash):
        try:
            tx = self.mongo_cli.get_one(
                table=FLAGS.transaction_info, cond={
                 FLAGS.tx_id: txhash})
        except Exception, e:
            raise exception.DBError(e)
        return tx

    def select_txin_by_hash(self, txhash):
        try:
            tx = self.mongo_cli.get_one(
                table=FLAGS.transaction_info, cond={
                    FLAGS.tx_id: txhash})
            txin = tx.get[FLAGS.transaction_in]
        except Exception, e:
            raise exception.DBError(e)
        return txin

    def select_txout_by_id(self, txout_id):
        try:
            txout = self.mongo_cli.get_one(
                table=FLAGS.transaction_info, cond={
                    FLAGS.txout_id: txout_id})
        except Exception, e:
            raise exception.DBError(e)
        return txout

    def select_txout_by_hash(self, txhash):
        try:
            tx = self.mongo_cli.get_one(
                table=FLAGS.transaction_info, cond={
                    FLAGS.tx_id: txhash})
            txouts = tx.get[FLAGS.transaction_out]
        except Exception, e:
            raise exception.DBError(e)
        return txouts
