#! /usr/bin/env python
# -*- coding: utf-8 -*-

from tools import flags
from driver.bytom.builtin import BuiltinDriver

FLAGS = flags.FLAGS


class TxManager():
    """Manages the tx query"""
    def __init__(self):
        self.driver = BuiltinDriver()

    # @CacheControl.cached(timeout=300, key_prefix='CACHE_TX')
    def handle_tx(self, tx_hash):
        try:
            tx_info = self.driver.request_tx_info(tx_hash)
            return tx_info
        except Exception, e:
            raise Exception("handle_tx error: %s", e)
