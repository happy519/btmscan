
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
            mainchain_list.reverse()
            return mainchain_list, height_record

       
        
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
            print str(transaction)+'\n'

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






    def rollback(self, block_height, block_num):
        self.set_mongo_recent_height(block_height-block_num)
        self.mongo_cli.delete_many(FLAGS.block_info, {FLAGS.block_height: {'$lte': block_height, '$gt': block_height-block_num}})
        self.mongo_cli.delete_many(FLAGS.address_info, {FLAGS.block_height: {'$lte': block_height, '$gt': block_height-block_num}})
        self.mongo_cli.delete_many(FLAGS.transaction_info, {FLAGS.block_height: {'$lte': block_height, '$gt': block_height-block_num}})
    