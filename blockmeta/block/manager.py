#! /usr/bin/env python
# -*- coding: utf-8 -*-

from tools import flags
from driver.bytom.builtin import BuiltinDriver
from blockmeta.constant import DISPLAY_LEN
from flask import current_app

FLAGS = flags.FLAGS


class BlockManager:
    """Manages the tx query"""
    def __init__(self):
        self.driver = BuiltinDriver()
        self.logger = current_app.logger

    def handle_block(self, block_id):
        try:
            block_info = self.driver.request_block_info(block_id)
            return block_info

        except Exception, e:
            self.logger.error("BlockManager.handle_block Error: %s" % str(e))
            raise Exception("handle_block error: %s", e)

    def list_blocks(self, start, offset):
        blocks = {}
        try:
            result = self.driver.list_blocks(start, offset)

            blocks['pages'] = offset / DISPLAY_LEN + 1
            blocks['blocks'] = result
            return blocks

        except Exception, e:
            self.logger.error("BlockManager.list_blocks Error: %s" % str(e))
            raise Exception("list_blocks error: %s", e)


