# -*- coding: utf-8 -*-
from flask_restful import Api
import blockmeta.address.api
import blockmeta.tx.api

#modules = [(handle, urls, args)]
MODULES = [
    # address
    (blockmeta.address.api.AddressAPI, ('/api/address/<string:addr_info>',), {'endpoint': 'address'}),
    (blockmeta.tx.api.TxAPI, ('/api/tx/<string:tx_hash>',), {'endpoint': 'tx'}),
]


def register_api(app):
    api = Api(app)
    for handle, urls, args in MODULES:
        api.add_resource(handle, *urls, **args)
