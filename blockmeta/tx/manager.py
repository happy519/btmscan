#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from flask import current_app
from flask import json
from blockmeta import db, exception, utils, flags, manager
from blockmeta.constant import EXPIRE_TIME, DISPLAY_LEN
from blockmeta import constant
from blockmeta.cache import CacheControl

FLAGS = flags.FLAGS


class TxManager(manager.Manager):
    """Manages the tx query"""

    def __init__(self, tx_driver=None, *args, **kwargs):
        if not tx_driver:
            tx_driver = FLAGS.tx_driver

        self.driver = utils.import_driver(tx_driver)
        self.cache = current_app.cache
        self.logger = current_app.logger
        super(TxManager, self).__init__(*args, **kwargs)

    @CacheControl.cached(timeout=300, key_prefix='CACHE_TX')
    def list_txs(self, start, offset, chain_type):

        txs = {}
        try:
            if chain_type == constant.BITCOIN:
                pass
            elif chain_type == constant.ETHEREUM or chain_type == constant.ETHEREUMCLASSIC:
                result, total_num = self.driver[chain_type].request_tx_info(start=start, offset=offset, detail=0)
                if result and total_num:
                    txs['pages'] = total_num / DISPLAY_LEN + 1
                    txs['txs'] = result
                return txs
            else:
                return txs

        except Exception, e:
            self.logger.error("TxManager.list_txs Error: %s" % str(e))
            raise Exception("list_txs error: %s", e)

    @CacheControl.cached(timeout=300, key_prefix='CACHE_TX')
    def handle_tx(self, tx_hash, detail, chain_type):

        result = {}
        try:
            if chain_type == constant.BYTOM:
                result = self.driver[chain_type].request_tx_info(tx_hash, detail)
                return result
            else:
                return result

        except Exception, e:
            self.logger.error("TxManager.handle_tx Error: %s" % str(e))
            raise Exception("handle_tx error: %s", e)

    def handle_mempool_tx(self, tx_hash):
        if not self.cache: return None
        try:
            key_pattern = "UNCONFIRMED_%s" % tx_hash
            mempool_str = self.cache.hash_get(key_pattern, 'detail')
            return eval(mempool_str) if mempool_str else mempool_str
        except Exception, e:
            self.logger.error(str(e))
            return None
