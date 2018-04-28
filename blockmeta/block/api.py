#! /usr/bin/env python
# -*- coding: utf-8 -*-

# from flask import current_app
from flask.ext.restful import Resource

from tools import flags
from manager import BlockManager
from blockmeta.constant import DEFAULT_OFFSET

FLAGS = flags.FLAGS


class BlockAPI(Resource):

    def __init__(self):
        self.manager = BlockManager()

    def get(self, block_id):
        print ("=======>>>>>>>>>>>>>>>>>>>>>"), block_id
        result = self.manager.handle_block(block_id) if block_id else {}
        return result


class BlockListAPI(Resource):

    def __init__(self):
        self.manager = BlockManager()

    def get(self, num=DEFAULT_OFFSET):
        result = self.manager.list_blocks(num)
        return result
