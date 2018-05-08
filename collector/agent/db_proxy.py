from collector.db.mongodriver import MongodbClient
from tools import flags
from tools import constant
from tools import  util

class DbProxy:

    def __init__(self):
        self.url_base = flags.FLAGS.bytomd_rpc

        self.mongo_cli = MongodbClient(host=flags.FLAGS.mongo_bytom_host, port=flags.FLAGS.mongo_bytom_port)
        self.mongo_cli.use_db(flags.FLAGS.mongo_bytom)

    def get_height(self):
        state = self.mongo_cli.get(flags.FLAGS.db_status)
        return None if state is None else state[flags.FLAGS.block_height]

    def set_height(self, height):
        self.mongo_cli.update_one(flags.FLAGS.db_status, {}, {'$set': {flags.FLAGS.block_height: height}}, True)

    def save_block(self, block):
        (block['fee'], block['coinbase']) = util.get_block_reward(block)
        self.mongo_cli.insert(flags.FLAGS.block_info, block)

        transactions = []
        for transaction in block['transactions']:
            transaction.update({'block_height': block['height'], 'block_hash': block['hash']})
            transactions.append(transaction)
        self.mongo_cli.insert_many(flags.FLAGS.transaction_info, transactions)
        self.index_address(transactions)

        self.set_height(block['height'])

    def index_address(self, transactions):
        address_dict = {}
        for transaction in transactions:
            for tx_input in transaction['inputs']:
                if tx_input['type'] != 'spend' or tx_input.get('asset_id').lower() != constant.BTM_ID:
                    continue

                address = tx_input.get('address', None)
                if address is None:
                    continue
                address_info = address_dict.get(address, None) or self.mongo_cli.get_one(flags.FLAGS.address_info,
                                                                                         {'address': address})
                if address_info is None:
                    raise Exception('transaction input address not existed in address collection: %s', address)

                address_info['balance'] -= tx_input['amount']
                address_info['sent'] += tx_input['amount']
                txs_set = set(address_info['txs'])
                if transaction['id'] not in txs_set:
                    address_info['txs'].append(transaction['id'])
                address_dict[address] = address_info

            for tx_output in transaction['outputs']:
                if tx_output.get('type') != 'control' or tx_output.get('asset_id').lower() != constant.BTM_ID:
                    continue

                address = tx_output.get('address')
                if not address:
                    continue

                address_info = address_dict.get(address, None) or self.mongo_cli.get_one(flags.FLAGS.address_info,
                                                                                         {'address': address})
                if address_info is None:
                    address_info = {
                        'address': address,
                        'balance': 0,
                        'recv': 0,
                        'sent': 0,
                        'txs': []
                    }
                address_info['balance'] += tx_output['amount']
                address_info['recv'] += tx_output['amount']
                txs_set = set(address_info['txs'])
                if transaction['id'] not in txs_set:
                    address_info['txs'].append(transaction['id'])
                address_dict[address] = address_info

        self.save_address_info(address_dict)

    def remove_highest_block(self, block):
        current_block_height = self.get_height()
        if current_block_height != block['height']:
            raise Exception('the block to be removed is not the highest one')

        self.mongo_cli.delete_one(flags.FLAGS.block_info, {'height': current_block_height})
        self.mongo_cli.delete_many(flags.FLAGS.transaction_info, {'height': current_block_height})
        self.rollback_address_info(block)

    def rollback_address_info(self, block):
        address_dict = {}
        for transaction in block['transactions']:
            for tx_input in transaction['inputs']:
                if tx_input['type'] != 'spend' or tx_input.get('asset_id').lower() != constant.BTM_ID:
                    continue

                address = tx_input.get('address')
                if not address:
                    continue

                address_info = address_dict.get(address, None) or self.mongo_cli.get_one(flags.FLAGS.address_info,
                                                                                         {'address': address})

                address_info['balance'] += tx_input['amount']
                address_info['sent'] -= tx_input['amount']
                address_info['txs'].remove(transaction['id'])
                address_dict[address] = address_info

            for tx_output in transaction['outputs']:
                if tx_output['type'] != 'control' or tx_output.get('asset_id').lower() != constant.BTM_ID:
                    continue

                address = tx_output.get('address')
                if not address:
                    continue

                address_info = address_dict.get(address, None) or self.mongo_cli.get_one(flags.FLAGS.address_info,
                                                                                         {'address': address})
                address_info['balance'] -= tx_output['amount']
                address_info['recv'] -= tx_output['amount']
                if transaction['id'] in address_info['txs']:
                    address_info['txs'].remove(transaction['id'])
                address_dict[address] = address_info

        self.save_address_info(address_dict)

    def save_address_info(self, address_dict):
        for key in address_dict:
            info = address_dict[key]
            self.mongo_cli.update_one(flags.FLAGS.address_info, {'address': info['address']}, {'$set': info}, True)

    def get_block_by_height(self, height):
        return self.mongo_cli.get_one(flags.FLAGS.block_info, {'height': height})
