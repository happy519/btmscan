#! /usr/bin/env python
# -*- coding: utf-8 -*-

from manager import AddressManager
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import flags
import sys

FLAGS = flags.FLAGS        


class AddressAPI(Resource):
    
    def __init__(self):
        self.manager = AddressManager()

    def get(self, addr_info=None):
        
        result = self.manager.handle_address(addr_info) if addr_info else {}    
        return result



