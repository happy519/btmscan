#! /usr/bin/env python
#coding=utf-8

import requests
import json
from copy import deepcopy
import flags
from db.mongodriver import MongodbClient
import log 

# from rollback_test_data import BLOCK_A, BLOCK_A_00, BLOCK_A_01, BLOCK_A_02, BLOCK_A_10, BLOCK_A_11
FLAGS = flags.FLAGS




# to do: status_fail: when status_fail == true, only update bytom asset


# need to save db height
class GetBytomDataAgent:
    def __init__(self):
        self.url_base = FLAGS.bytomd_rpc

        self.logger = log.init_log('agent')
        self.mongo_cli = MongodbClient(host=FLAGS.mongo_bytom_host, port=FLAGS.mongo_bytom_port)

        # to do : authentication is needed
        self.mongo_cli.use_db(FLAGS.mongo_bytom)
        self.mongo_recent_height = self.request_mongo_recent_height()


    def request_block_info(self, block_height):

        data_dict = {FLAGS.get_block_height_arg: block_height}
        url_rpc = self.url_base + '/' + FLAGS.get_block

        r = requests.post(url_rpc, json.dumps(data_dict))
        block_info =  get_data_part(r)
        return block_info

    def request_recent_height(self):
        # block id: 0 - recent_height
        url_rpc = self.url_base + '/' + FLAGS.get_block_count
        try:
            r = requests.post(url_rpc)
            chain_height = get_data_part(r)
            return chain_height[FLAGS.block_count]

        except Exception, e:
            self.logger.error("Agent.GetBytomDataAgent request_recent_height ERROR:" + str(e))
            raise Exception("request_recent_height error: %s" % str(e))
            return None

    def request_mongo_recent_height(self):
        height = None
        try:
            state = self.mongo_cli.get(FLAGS.db_status, {})

            if state is None:
                # self.mongo_recent_height = -1
                height = -1

            else:
                height = state[FLAGS.block_height]
                # print "ok! " + str(self.mongo_recent_height)

        except Exception, e:
            self.logger.error("Agent.GetBytomDataAgent request_mongo_recent_height ERROR:" + str(e))
            raise Exception("request_mongo_recent_height error: %s" % str(e))

        return height

    def set_mongo_recent_height(self, height):
        try:
            state = self.mongo_cli.update_one(FLAGS.db_status, {}, {'$set': {FLAGS.block_height: height}}, True)
        except Exception, e:
            self.logger.error("Agent.GetBytomDataAgent set_mongo_recent_height ERROR:" + str(e))
            raise Exception("set_mongo_recent_height error: %s" % str(e))

    def sync_all(self):
        while True and (self.mongo_recent_height is not None):

            recent_height = self.request_recent_height()

            if recent_height is not None:
                if recent_height < 0:
                    self.logger.error("Agent.GetBytomDataAgent sync_all gets negative recent_height ERROR:" + str(e))
                    raise Exception("sync_block get negative recent_height error: %s" % str(e))

                else:
                    self.logger.info('Recent block height in mainchain: '+str(recent_height)+'|| Recent block height in mongodb: '+str(self.mongo_recent_height))

                    while self.mongo_recent_height < recent_height:
                        next_height = self.mongo_recent_height + 1
                        block = agent.request_block_info(next_height)

                        # update mongodb
                        try:
                            self.logger.info('Syncing block: '+str(next_height))
                            print 'Syncing block: '+str(next_height)

                            agent.sync_block(block, recent_height)
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

    def rollback(self, block_height, block_num):
        self.set_mongo_recent_height(block_height-block_num)
        self.mongo_cli.delete_many(FLAGS.block_info, {FLAGS.block_height: {'$lte': block_height, '$gt': block_height-block_num}})
        self.mongo_cli.delete_many(FLAGS.address_info, {FLAGS.block_height: {'$lte': block_height, '$gt': block_height-block_num}})
        self.mongo_cli.delete_many(FLAGS.transaction_info, {FLAGS.block_height: {'$lte': block_height, '$gt': block_height-block_num}})
    
    def sync_block(self, block, recent_height):
        # data in mongodb should keep unique
        def update_blockdb(block_info):
            # if block_info exist, cover it; else insert
            print "---------------------------X-------------------------------"
            for block_info_element in block_info :
                self.logger.info('Inserting mainchain block of height ' + str(block_info_element[FLAGS.block_height]) + ': ' + str(block_info_element[FLAGS.block_id]))
                self.mongo_cli.insert_one(FLAGS.block_info, block_info_element)
                self.logger.info('Insert done!')
            
            print "---------------------------XX------------------------------"


        def update_addressdb(address_info):
            # if same address_info exists, cover it; else insert
            # if forked address_info exists, mark it as forked
            print "---------------------------X-------------------------------"
            for address_info_element in address_info :
                self.logger.info('Inserting addresses in mainchain block of height ' + str(address_info_element[FLAGS.block_height]) + ': ' + str(address_info_element[FLAGS.block_id]))
                self.mongo_cli.insert_one(FLAGS.address_info, address_info_element)
                self.logger.info('Insert done!')
            print "---------------------------XX-------------------------------"


        def update_transactiondb(transaction_info):
            # if block_info exist, cover it; else insert

            print "---------------------------X-------------------------------"
            for transaction_info_element in transaction_info :

                self.mongo_cli.insert_one(FLAGS.transaction_info, transaction_info_element)

            print "---------------------------XX------------------------------"



        def get_mainchainlist(block, recent_height):
        

            block_height = block[FLAGS.block_height]
            height_record = block_height
            mainchain_list = [block]

            if block_height > 1 and block_height == recent_height :
                block_height -= 1
                prevblock_hash = block[FLAGS.previous_block_hash]

                # need just get mainchain block of block_heigh and ignore forked block
                prevblock_db = self.mongo_cli.get(table=FLAGS.block_info, cond={FLAGS.block_height: block_height})
                prevblock_db_hash = prevblock_db[FLAGS.block_id] if prevblock_db else None

                # Can use != directly?
                while prevblock_db_hash is None or prevblock_db_hash != prevblock_hash :
                    

                    # for test
                    block = self.request_block_info(block_height)
                    mainchain_list.append(block)

                    block_height -= 1
                    prevblock_hash = block[FLAGS.previous_block_hash]

                    prevblock_db = self.mongo_cli.get(table=FLAGS.block_info, cond={FLAGS.block_height: block_height})
                    prevblock_db_hash = prevblock_db[FLAGS.block_id] if prevblock_db else None

            # reverse mainchain_list preventing empty middle block when server shuts down
            return mainchain_list.reverse(), height_record

        def info_abstract(mainchain_list):
            # pay attention to the change of block's keys
            block_info = mainchain_list

            address_info = []

            transaction_info = []

            for i, block in enumerate(mainchain_list) :
                txs = block[FLAGS.transactions]
                block_info[i][FLAGS.transactions] = []
                

                for j, tx in enumerate(txs):
                    block_info[i][FLAGS.transactions].append(tx[FLAGS.tx_id])

                    # Remeber to mark this
                    transaction_info_element = deepcopy(tx)
                    
                    transaction_info_element[FLAGS.block_id] = block[FLAGS.block_id]

                    transaction_info_element[FLAGS.block_height] = block[FLAGS.block_height]

                    transaction_info_element[FLAGS.coinbase] = False

                    # Remeber to mark this
                    # transaction_info_element = deepcopy(transaction_info_element)

                    for txin in tx[FLAGS.transaction_in]:
                        if txin[FLAGS.tx_io_type] == FLAGS.coinbase:
                        	transaction_info_element[FLAGS.coinbase] = True

                        if txin.has_key(FLAGS.address) and txin.has_key(FLAGS.asset_id) and txin.has_key(FLAGS.amount) and txin[FLAGS.amount] > 0 and txin.has_key(FLAGS.tx_i_id):
                            address_info_element = {
                                FLAGS.address : txin[FLAGS.address],
                                FLAGS.asset_id : txin[FLAGS.asset_id],
                                FLAGS.amount : txin[FLAGS.amount],
                                FLAGS.tx_io_type : txin[FLAGS.tx_io_type],
                                FLAGS.tx_io_id : txin[FLAGS.tx_i_id],
                                FLAGS.tx_id : tx[FLAGS.tx_id],
                                FLAGS.block_id : block[FLAGS.block_id],
                                FLAGS.block_height : block[FLAGS.block_height],
                                FLAGS.is_tx_in : True
                            }
                            address_info.append(address_info_element)


                    for txout in tx[FLAGS.transaction_out]:
                        if txout.has_key(FLAGS.address) and txout.has_key(FLAGS.asset_id) and txout.has_key(FLAGS.amount) and txout[FLAGS.amount] > 0 and txout.has_key(FLAGS.tx_o_id):
                            address_info_element = {
                                FLAGS.address : txout[FLAGS.address],
                                FLAGS.asset_id : txout[FLAGS.asset_id],
                                FLAGS.amount : txout[FLAGS.amount],
                                FLAGS.tx_io_type : txout[FLAGS.tx_io_type],
                                FLAGS.tx_io_id : txout[FLAGS.tx_o_id],
                                FLAGS.tx_id : tx[FLAGS.tx_id],
                                FLAGS.block_id : block[FLAGS.block_id],
                                FLAGS.block_height : block[FLAGS.block_height],
                                FLAGS.is_tx_in : False
                            }
                            address_info.append(address_info_element)
                    

                    
                    transaction_info.append(transaction_info_element)


            return (block_info, address_info, transaction_info)


        
        (mainchain_list, height_record) = get_mainchainlist(block, recent_height)
        print 'Length of maichain block pending: '+str(len(mainchain_list))
        self.rollback(height_record, len(mainchain_list))
        # ok
        (block_info, address_info, transaction_info) = info_abstract(mainchain_list)

        print '-----------------------Pending Block Info------------------------------'
        for block in block_info:
            print str(block)+'\n'

        print '------------------------------------------------------------------------'

        print '-----------------------Pending Address Info-----------------------------'
        for address in address_info:
            print str(address)+'\n'
        print '------------------------------------------------------------------------'

        print '-------------------------Pending Transaction Info-----------------------'
        for transaction in transaction_info:
            print str(tranaction)+'\n'

        print '-------------------------------------------------------------------------'
        
        self.logger.info('Obtain address info with '+str(len(address_info))+' txIO')
        self.logger.info('Adress info: '+str(address_info))

        
        try:
            print 'UPDATING BLOCK DB'
            update_blockdb(block_info)
            print 'END'
            print 'UPDATING TRANSACTION DB'
            update_transactiondb(transaction_info)
            print 'END'
            print 'UPDATING ADDRESS DB'
            update_addressdb(address_info)
            print 'END'



        except Exception, e:
            self.logger.error("Agent.GetBytomDataAgent update_db ERROR:" + str(e))
            raise Exception("update_db error: %s" % str(e))


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



