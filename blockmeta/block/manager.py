# -*- coding: utf-8 -*-

from flask import current_app

from blockmeta.constant import DISPLAY_LEN
from driver.bytom.builtin import BuiltinDriver
from tools import flags

FLAGS = flags.FLAGS


class BlockManager:
    """Manages the tx query"""
    def __init__(self):
        self.driver = BuiltinDriver()
        self.logger = current_app.logger

    def handle_block(self, block_id):
        try:
            return self.driver.request_block_info(block_id)
        except Exception, e:
            self.logger.error("BlockManager.handle_block Error: %s" % str(e))
            raise Exception("handle_block error: %s", e)

    def list_blocks(self, start, offset):
        blocks = {}
        try:
            result, total_num = self.driver.list_blocks(start, offset)
            blocks['pages'] = total_num / DISPLAY_LEN + 1
            blocks['blocks'] = result
            return blocks
        except Exception, e:
            self.logger.error("BlockManager.list_blocks Error: %s" % str(e))
            raise Exception("list_blocks error: %s", e)


