#! /usr/bin/env python
# -*- coding: utf-8 -*-

from tools import flags, exception
from blockmeta.tools.bytom import *
from blockmeta.db.mongo import MongodbClient
from blockmeta import constant

FLAGS = flags.FLAGS




# class Block_info():
#     def __init__(self, block_data):
#         reward = 41250000000.0
#         height = block_data[FLAGS.block_height]
#         n = min(height / 840000, 36)
#         for i in range(n):
#             reward /= 2
#
#         self.info = {
#             'pow': 1,
#             'hash': block_data[FLAGS.block_id],
#             'prev_block_hash': block_data[FLAGS.prev_block_hash] if block_data[FLAGS.block_height] != 0 else '',
#             'title': 'bytom'
#             'height': block_data[FLAGS.height],
#             'version': block_data[FLAGS.version],
#             'transaction_merkle_root': block_data[FLAGS.transaction_merkle_root],
#             'transaction_status_root':
#             block_data[FLAGS.transaction_status_root],
#             'time': block_data[FLAGS.timestamp],
#             'difficulty': block_data[FLAGS.difficulty],
#             'nbits': block_data[FLAGS.bits],
#             'relay': '',
#             'nonuce': block_data[
#                 FLAGS.nonuce],
#             'tx_num': len(block_data[FLAGS.transactions]),
#             'reward': reward,
#             'main': True,
#             'size':
#             block_data[FLAGS.block_size],
#             'tx': block_data[FLAGS.transactions],
#         }
#
#         get_info(self):
#         return self.info


# def block_validation(block_id, block_height):
#     return True


class BuiltinDriver(base.Base):
    @property
    def type(self):
        return 'bytom_builtin'

    def __init__(self):

        self.mongo_cli = MongodbClient(
            host=FLAGS.mongo_bytom_host,
            port=FLAGS.mongo_bytom_port)

        self.mongo_cli.use_db(FLAGS.mongo_bytom)

    def request_block_info(self, b_height=None, b_hash=None, start, offset, chain_id=1, basic=True):
        def abstract_info(block_data, chain):
            block_basic_info = Block_info(block_data, chain)
            return block_basic_info.get_info()

        try:
            if block_validation(b_height, b_hash) == False:
                raise Exception("address [%s] is not valid" % addr)

            # def get_all(self, table, cond={}, items=None, n=0, sort_key=None, ascend=True, skip=0)
            # consider situation of in main chain
            # take care of the type casting betweent mongodb and python

            block_data = {}
            if block_id is not None:
                block_data = self.mongo_cli.get_one(
                    table=FLAGS.block_info, cond={
                        FLAGS.block_id: block_id})
            else:
                block_data = self.mongo_cli.get_one(
                    table=FLAGS.block_info, cond={
                        FLAGS.block_height: block_height})

            block_basic_info = abstract_info(
                block_data, chain) if block_data else {}

            if basic:
                block_info = block_basic_info

            else:
                pass
                # get info of relevent transaction
                # 'values':           format_satoshis(value_out, chain),
                # 'tx_fees':          format_satoshis(block_fees, chain),

            return block_info

        except Exception, e:
            self.logger.error(
                "Block.BuiltinDriver.request_block_info Error: %s" %
                str(e))
            raise Exception("request_block_info error: %s", e)

    def list_blocks(self, start, offset):

        block_list = []
        blocks = self.mongo_cli.block_get_latest_in_range(
            start, DEFAULT_OFFSET)
        for block in blocks:
            block_info = Block_info(block).get_info()

            block_list.append(block_info)

        return block_list, block_list[0]['height'] + 1
