#! /usr/bin/env python
# coding=utf-8

import time

from collector.agent.fetcher import Fetcher
from collector.db.mongodriver import MongodbClient
from tools import flags, log
from collector.agent.db_proxy import DbProxy

FLAGS = flags.FLAGS


class DataAgent:
    sleep_time = 60

    def __init__(self):
        self.url_base = FLAGS.bytomd_rpc
        self.fetcher = Fetcher()
        self.proxy = DbProxy()

        self.logger = log.init_log('agent')
        self.mongo_cli = MongodbClient(host=FLAGS.mongo_bytom_host, port=FLAGS.mongo_bytom_port)

        self.mongo_cli.use_db(FLAGS.mongo_bytom)
        self.mongo_recent_height = self.proxy.get_height()

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
                    self.proxy.set_height(next_height)
                    self.mongo_recent_height = next_height
                except Exception, e:
                    self.logger.error("Agent.GetBytomDataAgent sync_block ERROR:" + str(e))
                    raise Exception("sync_block error: %s" % str(e))

            time.sleep(self.sleep_time)
