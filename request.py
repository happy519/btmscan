# -*- coding: utf-8 -*-

import requests
from mongodb import MongodbClient
import flags
import log
import json

FLAGS = flags.FLAGS


class RequestBytomd:
    def __init__(self):
        self.url_base = FLAGS.bytomd_rpc
        self.logger = log.init_log('agent')
        self.mongo_cli = MongodbClient(host=FLAGS.mongo_bytom_host, port=FLAGS.mongo_bytom_port)

        # todo : authentication is needed
        self.mongo_cli.use_db(FLAGS.mongo_bytom)
        self.mongo_recent_height = self.mongo_cli.request_recent_height()

    def block_info(self, height):
        data_dict = {FLAGS.get_block_height_arg: height}
        url_rpc = self.url_base + '/' + FLAGS.get_block

        r = requests.post(url_rpc, json.dumps(data_dict))
        block_info = get_data_part(r)
        return block_info

    def chain_height(self):
        url_rpc = self.url_base + '/' + FLAGS.get_block_count
        try:
            r = requests.post(url_rpc)
            print r.json()
            chain_height = get_data_part(r)
            # block id: 0 - recent_height
            return chain_height[FLAGS.block_count]
        except Exception, e:
            raise Exception("request_recent_height error: %s" % str(e))
            return None

    def tx_info(self, address):
        pass

    def account_info(self, address):
        pass



def get_data_part(msg):
        r = msg.json()
        return r[FLAGS.data]

