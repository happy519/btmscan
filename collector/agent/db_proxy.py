import copy

from collector.db.mongodriver import MongodbClient
from tools import flags


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
        # TODO: implement parse and save block process.
        # Make sure save block and set_height is atomic
        self.mongo_cli.insert(flags.FLAGS.db_block, block)
        self.mongo_cli.insert_many(flags.FLAGS.db_transaction, block['transactions'])

        address_dict = {}
        for tx in block['transactions']:
            for tx_input in tx['inputs']:
                if 'address' not in tx_input or 'amount' <= 0:
                    continue
                address_element = copy.deepcopy(tx_input)
                address_element['in'] = True
                address_element['tx_id'] = tx['id']
                address_element['block_id'] = block['hash']
                address_element['block_height'] = block['height']
                if 'address' in address_dict:
                    address_dict['address'].append(address_element)
                else:
                    address_dict = [address_element]

            for output in tx['outputs']:
                if 'address' not in tx_input and 'amount' > 0:
                    continue
                address_element = tx_input
                address_element['in'] = False
                address_element['tx_id'] = tx['id']
                address_element['block_id'] = block['hash']
                address_element['block_height'] = block['height']
                if 'address' in address_dict:
                    address_dict['address'].append(address_element)
                else:
                    address_dict['address'] = [address_element]

        address_info_list = []
        for address in address_dict:
            address_info = self.mongo_cli.get_one(flags.FLAGS.db_address, {'address': address})
            if address_info is None:
                address_info = {
                    'address': address,
                    'relevant_txo': address_dict[address]
                }

            else:
                address_info['relevant_txo'].append(address_dict[address])

            self.mongo_cli.update_one(flags.FLAGS.db_address, {'address': address}, {'$set': address_info}, True)

        self.set_height(block['height'])

    def index_address(self, transaction):
        address_dict = []
        for tx_input in transaction['inputs']:
            if tx_input['type'] != 'spend' or tx_input['asset_alias'].lower() != 'btm':
                continue

            address = tx_input['address']
            address_info = address_dict[address] or self.mongo_cli.get_one(flags.FLAGS.db_address, {'address': address})
            if address_info is None:
                raise Exception('transaction input address not existed in address collection: %s', address)

            address_info['balance'] -= tx_input['amount']
            address_info['sent'] += tx_input['amount']
            txs_set = set(address_info['txs'])
            if transaction['id'] not in txs_set:
                address_info['txs'].append(transaction['id'])
            address_dict[address] = address_info

        for tx_output in transaction['outputs']:
            if tx_output['type'] != 'control' or tx_output['asset_alias'].lower() != 'btm':
                continue

            address = tx_output['address']
            address_info = address_dict[address] or self.mongo_cli.get_one(flags.FLAGS.db_address, {'address': address})
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

        for key in address_dict:
            info = address_dict[key]
            self.mongo_cli.update_one(flags.FLAGS.db_address, {'address': info['address']}, {'$set': info}, True)

    def get_block_by_height(self, height):
        # TODO: implement it
        block = self.mongo_cli.get_one(flags.FLAGS.db_block, {'height': height})
        return block['block_info'] if block is not None else None
