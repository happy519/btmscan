#! /usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import os
import gflags
FLAGS = gflags.FLAGS

# manager
gflags.DEFINE_string('tx_manager', 'blockmeta.tx.manager.TxManager', '')


gflags.DEFINE_list('tx_driver', ['blockmeta.tx.driver.bytom.builtin.BuiltinDriver'], '')
gflags.DEFINE_string('db_driver', 'blockmeta.db.api', '')


# mongodb
gflags.DEFINE_bool('MONGODB_ENABLE', True, 'switch')
gflags.DEFINE_string('mongo_bytom_host', '127.0.0.1', 'mongodb host')
gflags.DEFINE_string('mongo_bytom_port',  27017, 'mongodb port')
gflags.DEFINE_string('mongo_bytom', 'bytom', 'mongodb bytom main db')
gflags.DEFINE_string('mongodb_user', 'bytom', 'mongodb user name')
gflags.DEFINE_string('mongodb_password', 'bytom', 'mongodb user password')
gflags.DEFINE_integer('table_capacity', 99000000, 'table capacity')




gflags.DEFINE_string('tx_id', 'id', '')
gflags.DEFINE_string('txout_id', 'outputs.id', 'txout id')
gflags.DEFINE_string('transaction_in', 'inputs', '')
gflags.DEFINE_string('transaction_out', 'outputs', '')
gflags.DEFINE_string('txin_id', 'inputs.id', 'txin id')

