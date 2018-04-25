#! /usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import os
import gflags
FLAGS = gflags.FLAGS


#manager
gflags.DEFINE_string('address_manager', 'blockmeta.address.manager.AddressManager', '')
gflags.DEFINE_string('block_manager',   'blockmeta.block.manager.BlockManager', '')
gflags.DEFINE_string('tx_manager',      'blockmeta.tx.manager.TxManager', '')
gflags.DEFINE_string('token_manager',   'blockmeta.token.manager.TokenManager', '')
gflags.DEFINE_string('search_manager',  'blockmeta.search.manager.SearchManager', '')
gflags.DEFINE_string('node_manager',    'blockmeta.node.manager.NodeManager', '')
gflags.DEFINE_string('rank_manager',    'blockmeta.rank.manager.RankManager', '')


gflags.DEFINE_string('db_driver',       'blockmeta.db.api', '')
gflags.DEFINE_string('merchant_driver', 'blockmeta.merchant.driver.builtin.BuiltinDriver',  '')
gflags.DEFINE_string('archives_driver', 'blockmeta.archives.driver.builtin.BuiltinDriver', '')


gflags.DEFINE_string('captcha_font_path', '../fonts', 'location of captcha font')


# log
gflags.DEFINE_string('DEBUG_LOG', 'logs/debug.log', 'location')
gflags.DEFINE_string('ERROR_LOG', 'logs/error.log', 'location')
gflags.DEFINE_string('INFO_LOG', 'logs/info.log', 'location')


#mongodb
gflags.DEFINE_string('mongo_btm_host', '127.0.0.1', 'mongodb host')
gflags.DEFINE_string('mongo_btm_port',  27017, 'mongodb port')

gflags.DEFINE_string('mongodb_user', 'abe', 'mongodb user')
gflags.DEFINE_string('mongodb_password', '14cZMQk89mRYQkDEj8Rn25AnGoBi5H6uer', 'mongodb host')

## database
gflags.DEFINE_string('mongo_btm', 'bytom', 'mongodb bytom main db')


# bitcoin mongo table setting
gflags.DEFINE_string('btc_addr_tx', 'address_tx', 'mongodb table')
gflags.DEFINE_string('btc_addr_info', 'pubkey_info', 'mongodb table')
gflags.DEFINE_string('btc_tx_value', 'tx_value', 'mongodb table')
gflags.DEFINE_string('btc_checkpoint', 'checkpoint', 'mongodb table')
gflags.DEFINE_string('btc_block_stat', 'block_stat', 'mongodb table')
gflags.DEFINE_string('btc_chain_stat', 'chain_stat', 'mongodb table')
gflags.DEFINE_string('btc_tx_stat', 'tx_stat', 'mongodb table')
gflags.DEFINE_string('btc_archives', 'archives', 'mongodb table')
gflags.DEFINE_string('btc_archive_stat', 'archive_stat', 'mongodb table')
gflags.DEFINE_string('btc_top_rank', 'top_rank', 'mongodb table')

# ethereum mongo table setting
gflags.DEFINE_string('blocks', 'blocks', 'mongodb table')
gflags.DEFINE_string('txs', 'txs', 'mongodb table')
gflags.DEFINE_string('accounts', 'accounts', 'mongodb table')
gflags.DEFINE_string('uncles', 'uncles', 'mongodb table')
gflags.DEFINE_string('token_basic', 'token_basic', 'mongodb table')
gflags.DEFINE_string('token_prefix', 'token_', 'mongodb table')
gflags.DEFINE_string('balance_prefix', 'balance_', 'mongodb table')
gflags.DEFINE_string('internal_tx_prefix', 'internalTxs', 'mongodb table')
gflags.DEFINE_integer('table_capacity', 99000000, 'table capacity')

#ticker
gflags.DEFINE_string('tk_okcoin', 'tk_okcoin_cn', 'okcoin')
gflags.DEFINE_string('tk_btcc', 'tk_btcc', 'btcc')
gflags.DEFINE_string('tk_huobi', 'tk_huobi', 'huobi')
gflags.DEFINE_string('tk_coinbase', 'tk_coinbase', 'mongodb table')



#test cmd
gflags.DEFINE_bool('test_all', False, 'switch')
gflags.DEFINE_list('test_case', [], 'test case')

#slice flag
gflags.DEFINE_bool('SLICE_ENABLE', False, 'switch')
gflags.DEFINE_integer('slice_size',  176000000, 'slice rule')




# agent
# bytomd RPC
gflags.DEFINE_string('bytomd_rpc', 'http://localhost:9888', '')
gflags.DEFINE_string('get_block', 'get-block', '')
gflags.DEFINE_string('get_block_height_arg', 'block_height', '')
gflags.DEFINE_string('get_block_count', 'get-block-count', '')
gflags.DEFINE_string('tx_i_id', 'spent_output_id', '')
gflags.DEFINE_string('tx_o_id', 'id', '')


gflags.DEFINE_bool('MONGODB_ENABLE', True, 'switch')
gflags.DEFINE_string('mongo_bytom_host', '127.0.0.1', 'mongodb host')
gflags.DEFINE_string('mongo_bytom_port',  27017, 'mongodb port')

# bytomd db
gflags.DEFINE_string('mongo_bytom', 'bytom', 'mongodb bytom main db')

# bytom table
gflags.DEFINE_string('db_status', 'status', '')
gflags.DEFINE_string('address_info', 'address_info', '')
gflags.DEFINE_string('block_info', 'block_info', '')
gflags.DEFINE_string('transaction_info', 'transaction_info', '')


# bytom table attributes
gflags.DEFINE_string('block_height', 'height', '')
gflags.DEFINE_string('block_count', 'block_count', '')
gflags.DEFINE_string('address', 'address', '')
gflags.DEFINE_string('block_hash', 'hash', '')
gflags.DEFINE_string('in_mainchain', 'in_mainchain', '')
gflags.DEFINE_string('previous_block_hash', 'previous_block_hash', '')
gflags.DEFINE_string('transactions', 'transactions', '')
gflags.DEFINE_string('transaction_in', 'inputs', '')
gflags.DEFINE_string('transaction_out', 'outputs', '')
gflags.DEFINE_string('asset_id', 'asset_id', '')
gflags.DEFINE_string('amount', 'amount', '')
gflags.DEFINE_string('tx_io_type', 'type', '')
gflags.DEFINE_string('tx_id', 'id', '')
gflags.DEFINE_string('is_tx_in', 'is_tx_in', '')
gflags.DEFINE_string('data', 'data', '')
gflags.DEFINE_string('tx_io_id', 'tx_io_id', '')

if __name__ == '__main__':
    print FLAGS.mongo_bytom_host
