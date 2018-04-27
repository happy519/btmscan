# -*- coding: utf-8 -*-
from flask_restful import Api
import blockmeta.address.api

#modules = [(handle, urls, args)]
MODULES = [
    # address
    (blockmeta.address.api.AddressAPI, ('/api/address/<string:addr_info>',), {'endpoint': 'address'}),
]




def register_api(app):
    api = Api(app)
    for handle, urls, args in MODULES:
        api.add_resource(handle, *urls, **args)





