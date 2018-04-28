#! /usr/bin/env python
# coding=utf-8

from blockmeta.db.mongo import MongodbClient
from tools import flags, exception

FLAGS = flags.FLAGS


class BuiltinDriver:
    @property
    def type(self):
        return 'builtin'
       
    def __init__(self):
        # self.logger = current_app.logger
        self.mongo_cli = MongodbClient(host=FLAGS.mongo_bytom_host, port=FLAGS.mongo_bytom_port)

        # TODO : authentication is needed
        self.mongo_cli.use_db(FLAGS.mongo_bytom)

    def request_address_info(self, addr):
        try:
            addr_object = self.get_info_by_addr(addr)
            if addr_object is None:
                Exception("Address not found!")
            addr_info = self._show_addr(addr_object)
        except Exception, e:
            raise Exception(e)
        return addr_info

    def get_info_by_addr(self, addr):
        try:
            address = self.mongo_cli.get_many(table=FLAGS.address_info, cond={FLAGS.address: addr})
            print "address: ", address
        except Exception, e:
            raise exception.DBError(e)
        return address

    def _show_addr(self, addr):
        delta = []
        tx_list = []
        asset_map = {}  # all assets stored in this map

        for utxo in addr:
            is_in = utxo.get(FLAGS.is_tx_in)
            amount = utxo.get(FLAGS.amount)
            tx_id = utxo.get(FLAGS.tx_id)
            asset_id = utxo.get(FLAGS.asset_id)

            money = amount * -1 if is_in else amount
            delta.append(money)
            tx_list.append(tx_id)

            if asset_id not in asset_map:
                asset_map[asset_id] = money
            else:
                asset_map[asset_id] += money

        balance = 0
        rev = 0
        sent = 0
        for x in delta:
            balance += x
            if x > 0:
                rev += x
            else:
                sent -= x

        tx_num = len(addr)
        address = addr[0].get(FLAGS.address)

        # TODO multi asset, one asset one map
        addr_info = {
            'balance': balance,
            'rev': rev,
            'sent': sent,
            'tx_num': tx_num,
            'addr': address,
            'assets': asset_map,
            'transactions': tx_list
        }
        return addr_info
