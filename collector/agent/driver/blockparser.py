

class BlockParser:
    def __init__(self, block = {}):
        self.block = block

        self.block_info = {}
        self.transaction_info = []
        self.address_info = []
        self.asset_info = []


    def parse(self):
        # pay attention to the change of block's keys
        self.block_info = deepcopy(self.block)

        txs = block[FLAGS.transactions]
        self.block_info[FLAGS.transactions] = []  

        for tx in txs:
            self.block_info[FLAGS.transactions].append(tx[FLAGS.tx_id])

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

                if FLAGS.address in txin and FLAGS.asset_id in txin and FLAGS.amount in txin and txin[FLAGS.amount] > 0 and FLAGS.tx_i_id in txin:
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
                    self.address_info.append(address_info_element)


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
                    self.address_info.append(address_info_element)
            

            
            self.transaction_info.append(transaction_info_element)
