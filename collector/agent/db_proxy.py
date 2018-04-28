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

                "inputs": [
                    {
                        "type": "coinbase",
                        "asset_id": "0000000000000000000000000000000000000000000000000000000000000000",
                        "asset_definition": { },
                        "amount": 0,
                        "arbitrary": "e29ba3"
                    }
                ],
                "outputs": [
                    {
                        "type": "control",
                        "id": "400cfcfd02cb8d64fca23c905ee76855e34883979c762b2e55bba3cd4002b645",
                        "position": 0,
                        "asset_id": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
                        "asset_definition": { },
                        "amount": 42250000000,
                        "control_program": "0014b2a40d1a9a67de553f34475a7759e1e4f31a2ad1",
                        "address": "bm1qk2jq6x56vl0920e5gad8wk0pune352k3c59cp7"
                    }
                ],

    def save_block(self, block):
        # TODO: implement parse and save block process.
        # Make sure save block and set_height is atomic


        self.mongo_cli.insert_many(flags.FLAGS.db_block, [{'block_id': block['hash'], 'block_info': block}, {'block_height': block['height'], 'block_info': block}])
        
        self.mongo_cli.insert_many(flags.FLAGS.db_transaction, block['transactions'])

        address_dict = {}

        for tx in block['transactions']:
            for input in tx['inputs']:
                if 'address' not in input or 'amount' <= 0:
                    continue
                address_element = input
                address_element['in'] = True
                address_element['tx_id'] = tx['id']
                address_element['block_id'] = block['hash']
                address_element['block_height'] = block['height']
                if 'address' in address_dict:
                    address_dict['address'].append(address_element)
                else:
                    address_dict = [address_element]


            for output in tx['outputs']:
                if 'address' not in input and 'amount' > 0:
                    continue
                address_element = input
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
                    'address': key,
                    'relevant_txo': address_dict[key] 
                }

            else:   
                address_info['relevant_txo'].append(address_dict[key])

             self.mongo_cli.update_one(flags.FLAGS.db_address, {'address': address}, {'$set': address_info}, True)

        self.set_height(block['height'])

    def get_block_by_height(self, height):
        # TODO: implement it
        block = self.mongo_cli.get_one(flags.FLAGS.db_block, {'height': height})
        return block['block_info'] if block is not None else None
