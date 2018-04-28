#! /usr/bin/env python
#coding=utf-8

import requests
import json
from copy import deepcopy
from collector import flags, log
from collector.db.mongodriver import MongodbClient
import time

# from rollback_test_data import BLOCK_A, BLOCK_A_00, BLOCK_A_01, BLOCK_A_02, BLOCK_A_10, BLOCK_A_11
FLAGS = flags.FLAGS




# to do: status_fail: when status_fail == true, only update bytom asset


# need to save db height
class DataAgent:
    def __init__(self):
        self.url_base = FLAGS.bytomd_rpc

        self.logger = log.init_log('agent')
        self.mongo_cli = MongodbClient(host=FLAGS.mongo_bytom_host, port=FLAGS.mongo_bytom_port)

        # to do : authentication is needed
        self.mongo_cli.use_db(FLAGS.mongo_bytom)
        self.mongo_recent_height = self.request_mongo_recent_height()


    def sync_all(self):
        while True and (self.mongo_recent_height is not None):

            recent_height = self.request_recent_height()
            print 'recent_height: '+str(recent_height)
            if recent_height is not None:
                if recent_height < 0:
                    self.logger.error("Agent.GetBytomDataAgent sync_all gets negative recent_height ERROR:" + str(e))
                    raise Exception("sync_block get negative recent_height error: %s" % str(e))

                else:
                    self.logger.info('Recent block height in mainchain: '+str(recent_height)+'|| Recent block height in mongodb: '+str(self.mongo_recent_height))

                    while self.mongo_recent_height < recent_height:
                        next_height = self.mongo_recent_height + 1
                        block = self.request_block_info(next_height)

                        # update mongodb
                        try:
                            self.logger.info('Syncing block: '+str(next_height))
                            print 'Syncing block: '+str(next_height)

                            self.sync_block(block, recent_height)
                            self.logger.info("Sync done: " + str(next_height))
                            print "Sync done: " + str(next_height)

                            self.logger.info("Updating block height in mongodb to "+str(next_height))
                            print "Updating block height in mongodb to "+str(next_height)
                            self.set_mongo_recent_height(next_height)
                            self.logger.info("Update done!")
                            print "Update done!"
                            self.mongo_recent_height = next_height

                        # need to know how to deal with exception
                        except Exception, e:
                            self.logger.error("Agent.GetBytomDataAgent sync_block ERROR:" + str(e))
                            raise Exception("sync_block error: %s" % str(e))



            time.sleep(self.sleep_time())

 


    def sleep_time(self):
        return 60


def get_data_part(msg):
    r = msg.json()
    return r[FLAGS.data]

# def print_transaction(tx):
# 	print '-------------------'
# 	print 'block_id: '+str(tx[FLAGS.block_id])
# 	print 'tx_id: '+str(tx[FLAGS.tx_id])
# 	print 'height: '+str(tx[FLAGS.block_height])
# 	print 'coinbase: '+str(tx[FLAGS.coinbase])
# 	print '-------------------'



