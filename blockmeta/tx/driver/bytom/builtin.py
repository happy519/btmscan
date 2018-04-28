#! /usr/bin/env python
# -*- coding: utf-8 -*-


from tools import flags, exception
from blockmeta.db.mongo import MongodbClient
from blockmeta import constant
from blockmeta.tools.bytom import remove_0x

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
            tx = self.get_tx_by_hash(remove_0x(tx_hash))
            if tx is None:
                raise Exception("Transaction not found!")

            tx_info = self._show_tx(tx)
        except Exception, e:
            raise Exception(e)
        return tx_info

    def get_tx_list(self, offset):
        try:
            tx_list = []
            txs = self.mongo_cli.get_last_n(table=FLAGS.transaction_info, args=None, order=FLAGS.block_height, n=offset)
            for tx in txs:
                tx_info = self._show_tx(tx)
                tx_list.append(tx_info)

        except Exception, e:
            raise exception.DBError(e)
        return tx_list

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

    def _show_tx(self, tx):
        tx_info = {}
        tx_id = tx.get(FLAGS.tx_id)
        tx_version = tx.get(FLAGS.version)
        block_height = tx.get(FLAGS.block_height)
        tx_in = tx.get(FLAGS.transaction_in)
        tx_out = tx.get(FLAGS.transaction_out)
        tx_size = tx.get(FLAGS.size)
        is_coinbase = tx.get(FLAGS.coinbase)
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
        if is_coinbase:
            tx_fee = 0

        tx_info['tx_id'] = tx_id
        tx_info['version'] = tx_version
        tx_info['block_height'] = block_height
        tx_info['value_in'] = value_in
        tx_info['value_out'] = value_out
        tx_info['fee'] = tx_fee
        tx_info['size'] = tx_size
        tx_info['is_coinbase'] = is_coinbase
        tx_info['txin'] = tx_in
        tx_info['txout'] = tx_out

        return tx_info
