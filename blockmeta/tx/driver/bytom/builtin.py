#! /usr/bin/env python
# -*- coding: utf-8 -*-


from tools import flags, exception
from blockmeta.tools.bytom import *
from blockmeta.db.mongo import MongodbClient

FLAGS = flags.FLAGS


class BuiltinDriver():
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
                raise Exception("Transcation not found")

            tx_id = tx.get(FLAGS.tx_id)
            tx_version = tx.get(FLAGS.tx_id)
            block_height = tx.get(FLAGS.block_height)

            tx_info['tx_id'] = tx_id
            tx_info['version'] = tx_version
            tx_info['block_height'] = block_height

            return tx_info
        except Exception, e:
            raise Exception(e)

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
            LOG.debug("select_txout_by_id: %s" % str(e))
            raise exception.DBError(e)
        return txout

    def select_txout_by_hash(self, txhash):
        try:
            tx = self.mongo_cli.get_one(
                table=FLAGS.transaction_info, cond={
                    FLAGS.tx_id: txhash})
            txouts = tx.get[FLAGS.transaction_out]
        except Exception, e:
            LOG.debug("select_txout_by_hash: %s" % str(e))
            raise exception.DBError(e)
        return txouts
