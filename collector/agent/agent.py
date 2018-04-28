#! /usr/bin/env python
# coding=utf-8

import time

from collector.agent.fetcher import Fetcher
from collector.db.mongodriver import MongodbClient
from tools import flags, log

# from rollback_test_data import BLOCK_A, BLOCK_A_00, BLOCK_A_01, BLOCK_A_02, BLOCK_A_10, BLOCK_A_11
FLAGS = flags.FLAGS

# to do: status_fail: when status_fail == true, only update bytom asset


# need to save db height
class DataAgent:
    sleep_time = 60

    def __init__(self):
        self.url_base = FLAGS.bytomd_rpc
        self.fetcher = Fetcher()

        self.logger = log.init_log('agent')
        self.mongo_cli = MongodbClient(host=FLAGS.mongo_bytom_host, port=FLAGS.mongo_bytom_port)

        self.mongo_cli.use_db(FLAGS.mongo_bytom)
        self.mongo_recent_height = self.request_mongo_recent_height()

    def request_mongo_recent_height(self):
        try:
            state = self.mongo_cli.get(FLAGS.db_status, {})
            return None if state is None else state[FLAGS.block_height]
        except Exception, e:
            raise Exception("request_mongo_recent_height error: %s" % str(e))

    def set_mongo_recent_height(self, height):
        try:
            self.mongo_cli.update_one(FLAGS.db_status, {}, {'$set': {FLAGS.block_height: height}}, True)
        except Exception, e:
            self.logger.error("Agent.GetBytomDataAgent set_mongo_recent_height ERROR:" + str(e))
            raise Exception("set_mongo_recent_height error: %s" % str(e))

    def sync_all(self):
        if self.mongo_recent_height is None:
            # TODO: request the block whose height is 0
            pass

        while True:
            recent_height = self.fetcher.request_chain_height()
            if recent_height is None:
                time.sleep(self.sleep_time)
                # TODO: request and save the block whose height is 0
                continue

            while self.mongo_recent_height < recent_height:
                # TODO: find the sync begining height
                next_height = self.mongo_recent_height + 1
                block = self.fetcher.request_block(next_height)

                try:
                    self.sync_block(block, recent_height)
                    self.set_mongo_recent_height(next_height)
                    self.mongo_recent_height = next_height
                except Exception, e:
                    self.logger.error("Agent.GetBytomDataAgent sync_block ERROR:" + str(e))
                    raise Exception("sync_block error: %s" % str(e))

            time.sleep(self.sleep_time)


def get_data_part(msg):
    r = msg.json()
    return r[FLAGS.data]
