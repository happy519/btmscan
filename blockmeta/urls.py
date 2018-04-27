# -*- coding: utf-8 -*-
from flask_restful import Api
import blockmeta.address.api
import blockmeta.tx.api

#modules = [(handle, urls, args)]
MODULES = [
    # address
    (blockmeta.address.api.AddressAPI, ('/api/address/<string:addr_info>',), {'endpoint': 'address'}),

    # tx
    (blockmeta.tx.api.TxAPI, ('/api/tx/<string:tx_hash>',), {'endpoint': 'tx'}),
    (blockmeta.tx.api.TxListAPI, ('/api/txs',), {'endpoint': 'txs'}),
]


def register_api(app):
    api = Api(app)
    for handle, urls, args in MODULES:
        api.add_resource(handle, *urls, **args)
