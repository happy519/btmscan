#! /usr/bin/env python
# -*- coding: utf-8 -*-

from tools import flags
from driver.bytom.builtin import BuiltinDriver

FLAGS = flags.FLAGS


class BlockManager:
    """Manages the tx query"""
    def __init__(self):
        self.driver = BuiltinDriver()

    def handle_block(self, block_id):
        try:
            block_info = self.driver.request_block_info(block_id)
        except Exception, e:
            raise Exception("handle_block error: %s", e)
        return block_info

    def list_blocks(self, num):
        try:
            blocks = self.driver.list_blocks(num)
        except Exception, e:
            raise Exception("list_blocks error: %s", e)
        return blocks
