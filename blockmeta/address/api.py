#! /usr/bin/env python
# -*- coding: utf-8 -*-

from manager import AddressManager
from flask_restful import Resource
from tools import flags

FLAGS = flags.FLAGS        


class AddressAPI(Resource):
    
    def __init__(self):
        self.manager = AddressManager()

    def get(self, address):
        
        result = self.manager.handle_address(address) if address else {}
        return result
