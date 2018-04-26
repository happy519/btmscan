import sys
from constant import BYTOM_ASSET_ID
from bson.objectid import ObjectId
from db.mongodriver import MongodbClient


import flags
FLAGS = flags.FLAGS



class Asset_info:
    def __init__(self, balance = 0, recv = 0, tx_num = 0, addr = ''):
        self.info = {}
        self.info['balance'] = int(balance)
        self.info['recv'] = int(recv)
        self.info['sent'] = int(recv) - int(balance)
        self.info['addr'] = addr
        self.info['txs'] = {}

    def get_info(self):
        txs_list = []
        if self.info['txs'] != {} :
            for key, value in self.info['txs'].items():
                txs_list.append(value)

            # show newest transactions first
            
        txs_list.sort(key=lambda obj: obj.get('height'), reverse=True)
        info = {
            'balance': self.info['balance'],
            'recv': self.info['recv'],
            'sent': self.info['sent'],
            'addr': self.info['addr'],
            'txnum' : len(txs_list),
            'txs': txs_list

        }

        return info

    def update(self, address_info_element):

        delta = int(address_info_element[FLAGS.amount])
        if address_info_element[FLAGS.is_tx_in]:
            delta = -delta
        self.info['balance'] += delta
        self.info['recv'] += delta
        self.info['sent'] = self.info['recv'] - self.info['balance']
        self.info['addr'] = address_info_element[FLAGS.address]

        if address_info_element[FLAGS.tx_id] in self.info['txs'].keys():
            self.info['txs'][address_info_element[FLAGS.tx_id]]['balance_change'] += delta
        else:
            self.info['txs'][address_info_element[FLAGS.tx_id]] = {
                'tx_id': address_info_element[FLAGS.tx_id], 
                'block_id': address_info_element[FLAGS.block_id],
                'height': address_info_element[FLAGS.block_height],
                'balance_change': delta
            }

def address_validation(addr):
    return True



# class BuiltinDriver(base.Base):
class BuiltinDriver():
    @property
    def type(self):
        return 'bytom_builtin'
       
    def __init__(self):
        # self.logger = current_app.logger
        self.mongo_cli = MongodbClient(host=FLAGS.mongo_bytom_host, port=FLAGS.mongo_bytom_port)

        # to do : authentication is needed
        self.mongo_cli.use_db(FLAGS.mongo_bytom)

    
    def request_address_info(self, addr):
        def abstract_info(addr_data):
            addr_info = {}
            for addr_data_element in addr_data:
                if addr_data_element[FLAGS.asset_id] not in addr_info.keys():
                    addr_info[addr_data_element[FLAGS.asset_id]] = Asset_info()
                addr_info[addr_data_element[FLAGS.asset_id]].update(addr_data_element)

            
            result = {}
            for key, value in addr_info.items():
                result[key] = value.get_info()

            return result


        # try:
        if address_validation(addr) == False:
            raise Exception("address [%s] is not valid" % addr)

        # def get_all(self, table, cond={}, items=None, n=0, sort_key=None, ascend=True, skip=0)
        # consider situation of in main chain
        # take care of the type casting betweent mongodb and python
        addr_data = self.mongo_cli.get_all(table=FLAGS.address_info, cond={FLAGS.address: addr})
        addr_info = abstract_info(addr_data)
        
        # show BYTOM default
        if BYTOM_ASSET_ID not in addr_info.keys():
            addr_info[BYTOM_ASSET_ID] = Asset_info(addr=addr).get_info()

        return addr_info

        # except Exception, e:
        #     # self.logger.error("Address.BuiltinDriver request_address_info ERROR:" + str(e))
        #     raise Exception("request_address_info error: %s" % str(e))   


if __name__ == "__main__":
    FLAGS(sys.argv)
    demo = BuiltinDriver()
    result = demo.request_address_info('tm1q6jxakzk8xcfz0qazqsltft209s4gn3lgh3tlam')
    print result

#     test = []
#     test_element1 = {
#         "_id": ObjectId("5add783605029421d6a45c74"),
#         "id": "228176668d8260b5b79c1e8c8c6673f9bd4c247feb0efbc6c708aad256b91c78",
#         "is_tx_in": False,
#         "tx_io_id": "8bb71b051ade652a62983a71abc221ad5404b62b900c97902be487a5f2d9a294",
#         "asset_id": "tm1qu539ugqzszgl084j60re6d9np8atdx0kfml0z4",
#         "amount": long("41250000000"),
#         "hash": "3dca0303a289e50460b4f0033ac10ea06f02f01dafce05cce0acd5fb98b0b0c8",
#         "in_mainchain": True,
#         "address": "tm1qu539ugqzszgl084j60re6d9np8atdx0kfml0z4",
#         "type": "control",
#         "height": 22
#     }


#     test_element2 = {
#         "_id": ObjectId("5add783605029421d6a45c74"),
#         "id": "228176668d8260b5b79c1e8c8c6673f9bd4c247feb0efbc6c708aad256b91c78",
#         "is_tx_in": True,
#         "tx_io_id": "8bb71b051ade652a62983a71abc221ad5404b62b900c97902be487a5f2d9a294",
#         "asset_id": "tm1qu539ugqzszgl084j60re6d9np8atdx0kfml0z4",
#         "amount": long("41250000000"),
#         "hash": "3dca0303a289e50460b4f0033ac10ea06f02f01dafce05cce0acd5fb98b0b0c8",
#         "in_mainchain": True,
#         "address": "tm1qu539ugqzszgl084j60re6d9np8atdx0kfml0z4",
#         "type": "control",
#         "height": 22
#     }

#     test_element3 = {
#         "_id": ObjectId("5add783605029421d6a45c74"),
#         "id": "131476668d8260b5b79c1e8c8c6673f9bd4c247feb0efbc6c708aad256b91c78",
#         "is_tx_in": False,
#         "tx_io_id": "8bb71b051ade652a62983a71abc221ad5404b62b900c97902be487a5f2d9a294",
#         "asset_id": "tm1qu539ugqzszgl084j60re6d9np8atdx0kfml0z4",
#         "amount": long("1"),
#         "hash": "3dca0303a289e50460b4f0033ac10ea06f02f01dafce05cce0acd5fb98b0b0c8",
#         "in_mainchain": True,
#         "address": "tm1qu539ugqzszgl084j60re6d9np8atdx0kfml0z4",
#         "type": "control",
#         "height": 44
#     }

#     test_element4 = {
#         "_id": ObjectId("5add783605029421d6a45c74"),
#         "id": "245676668d8260b5b79c1e8c8c6673f9bd4c247feb0efbc6c708aad256b91c78",
#         "is_tx_in": False,
#         "tx_io_id": "8bb71b051ade652a62983a71abc221ad5404b62b900c97902be487a5f2d9a294",
#         "asset_id": "tm1qu539ugqzszgl084j60re6d9np8atdx0kfml0z4",
#         "amount": long("2"),
#         "hash": "3dca0303a289e50460b4f0033ac10ea06f02f01dafce05cce0acd5fb98b0b0c8",
#         "in_mainchain": True,
#         "address": "tm1qu539ugqzszgl084j60re6d9np8atdx0kfml0z4",
#         "type": "control",
#         "height": 0
#     }

#     test_element5 = {
#         "_id": ObjectId("5adedb4d3c1b60f9d44f75c7"),
#         "id": "88f140c49c404fdaa25f385784cec7eec603aaa1933731f7888a6100d2735ca2",
#         "is_tx_in": False,
#         "tx_io_id": "a511aca850c71422a871e94a05a0e578c1abaa7a671d6111efbb16ada2b3961f",
#         "asset_id": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
#         "amount": 10,
#         "hash": "abfecf9d5150f96d7e54396b14b8587c5e9a2fc76c4eb6d95c11a2d46022cf15",
#         "in_mainchain": True,
#         "address": "tm1qvujkjf8q832c7g60qgacmef59ea8q2zelaa0z5",
#         "type": "control",
#         "height": 531
#     }


#     test.append(test_element1)
#     test.append(test_element2)
#     test.append(test_element3)
#     test.append(test_element4)
#     # test.append(test_element5)

    
#     demo = BuiltinDriver()
#     result = demo.request_address_info('doublespending', test)
#     print result





        
    # def request_confirmed_txs(self, addr, start, end, filter):        
        
    #     try:
    #         txs = []    
    #         addr_set = set()    

    #         if self.address_validation(addr) :
    #             raise Exception("address [%s] is not valid" % addr)
            
    #         # Or we can use for loop until len(txs)=min(num, n=end-start+1)
    #         # start, end should be constrainted
    #         tx_list_all = self.mongo_cli.get(table=FLAGS.bytom_addr_tx, args={'address_id': addr})
            
    #         tx_list = self._process_filter(tx_list_all, addr, start, end, filter)
    #         for tx_data in tx_list:   
    #             tx = self.tx_handler(tx_data)
    #             txs.append(tx)
                                
    #         txs = sorted([t for t in txs if t], key=itemgetter('tx_time'), reverse=True) 
    #         return txs
    #     except Exception, e:
    #         self.logger.error("Address.BuiltinDriver request_confirmed_txs ERROR:" + str(e))
    #         raise Exception("request_confirmed_txs error: %s" % str(e))           
    
    # #repair
    # def request_unconfirmed_txs(self, address, start=0, end=10): 

    #     try:
    #         unconfirmed_value = 0
    #         txs = []      
            
    #         return {'unconfirmed_txs': txs,
    #                 'unconfirmed_value':  unconfirmed_value}
    #     except Exception, e:
    #         self.logger.error("Address.BuiltinDriver request_unconfirmed_txs ERROR:" + str(e))
    #         return None    
    

    # def tx_handler(self, tx_hash, ntime, chain, dbhash, addr, is_p2sh, main, addr_set):
    #     tx_info = {}
                
    #     tx_info['filter'] =         filter
    #     tx_info['tx_value'] =       '+'+format_bitcoin_satoshis(tx_value) if tx_value > 0 else format_bitcoin_satoshis(tx_value)
    #     tx_info['inputs'] =         inputs if inputs else coinbase_inputs
    #     tx_info['outputs'] =        outputs 
    #     tx_info['total_input'] =    format_bitcoin_satoshis(value_out)
    #     tx_info['total_output'] =   format_bitcoin_satoshis(value_in)
    #     tx_info['fee'] =            format_bitcoin_satoshis(0 if tx_pos==0 else
    #                                     (value_in and value_out and value_out - value_in))
    #     tx_info['tx_time']      =   int(tx_time) if tx_time else int(ntime)
    #     tx_info['block_height'] =   int(height)
    #     tx_info['confirmation'] =   int(bheight) - int(height) + 1 if main else -1
    #     tx_info['is_coinbase'] =    1 if tx_pos==0 else 0
    #     tx_info['hash'] =           hashout_hex(tx_hash)
    #     tx_info['long'] =           long
    #     return tx_info

 
    
    # #############private ####
    # def _process_filter(tx_list_all, addr, start, end, filter):

    #     tx_list, sent_list = stat.get('tx_list', []), stat.get('sent_list', [])
    #     if filter == FILTER_SENT:
    #         ids = [i for i, sent in enumerate(sent_list) if sent==1]
    #         ids.reverse()
    #         return [tx_list[i] for i in ids[start:end]]
        
    #     if filter == FILTER_RECEIVED:
    #         ids = [i for i, sent in enumerate(sent_list) if sent==0]
    #         ids.reverse()            
    #         return [tx_list[i] for i in ids[start:end]]
 
    #     if filter == FILTER_UNSPENT:
    #         spent_txs = self.db.address_unspent_get_tx_id(dbhash)
    #         ids = [tx_id for i, tx_id in enumerate(tx_list) if sent_list[i]==0 and tx_id not in spent_txs]
    #         ids.reverse()
    #         return ids[start:end]
        
    #     tx_list.reverse()
    #     return tx_list[start:end]
