#! /usr/bin/env python
# -*- coding: utf-8 -*-

from tools import flags, exception
from blockmeta.tools.bytom import is_hash_prefix, remove_0x
from blockmeta.db.mongo import MongodbClient
from blockmeta.constant import DEFAULT_OFFSET

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

    def request_block_info(self, arg):
        try:
            block_id = remove_0x(arg)
            if len(block_id) == 64:
                block_info = self.get_block_by_hash(block_id)
            else:
                block_info = self.get_block_by_height(block_id)

        except Exception as e:
            raise Exception("request_block_info error: %s", e)
        return block_info

    def list_blocks(self, offset=DEFAULT_OFFSET):
        try:
            block_list = []
            blocks = self.get_block_latest_in_range(offset)
            for block in blocks:
                block_info = self._show_block(block)
                block_list.append(block_info)

        except Exception as e:
            raise Exception("list_blocks error: %s", e)
        return block_list

    def get_block_by_height(self, height):
        try:
            if int(height) < 0:
                raise Exception("Block height is wrong!")
            block = self.mongo_cli.get_one(
                table=FLAGS.block_info, cond={
                    FLAGS.block_height: int(height)})
            if block is None:
                raise Exception("Block not found!")
            block_info = self._show_block(block)

        except Exception as e:
            raise exception.DBError(e)
        return block_info

    def get_block_by_hash(self, blockhash):
        try:
            if not is_hash_prefix(blockhash):
                raise Exception("Block hash is wrong!")
            block = self.mongo_cli.get_one(
                table=FLAGS.block_info, cond={
                    FLAGS.block_id: blockhash})
            if block is None:
                raise Exception("Block not found!")
            block_info = self._show_block(block)
        except Exception as e:
            raise exception.DBError(e)
        return block_info

    def get_block_latest_in_range(self, offset):
        try:
            blocks = self.mongo_cli.get_last_n(
                table=FLAGS.block_info,
                args=None,
                order=FLAGS.block_height,
                n=offset)
        except Exception as e:
            raise exception.DBError(e)
        return blocks

    def _show_block(self, block):
        '''
        format conversion
        convert to the block message that user see
        :param block: block from db
        :return:
        '''
        block_info = {}
        block_height = block.get(FLAGS.block_height)
        block_hash = block.get(FLAGS.block_id)
        block_version = block.get(FLAGS.version)
        pre_block_hash = block.get(FLAGS.previous_block_hash)
        tx_merkle_root = block.get(FLAGS.merkle_root)
        nonce = block.get(FLAGS.nonce)
        timestamp = block.get(FLAGS.timestamp)
        difficulty = block.get(FLAGS.difficulty)
        nbit = block.get(FLAGS.block_nbit)
        transactions = block.get(FLAGS.transactions)
        block_size = block.get(FLAGS.block_size)

        block_info['block_height'] = block_height
        block_info['block_hash'] = block_hash
        block_info['block_version'] = block_version
        block_info['pre_block_hash'] = pre_block_hash
        block_info['tx_merkle_root'] = tx_merkle_root
        block_info['nonce'] = nonce
        block_info['timestamp'] = timestamp
        block_info['difficulty'] = difficulty
        block_info['nbit'] = nbit
        block_info['transactions'] = transactions
        block_info['block_size'] = block_size

        return block_info
