#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from driver.bytom.builtin import BuiltinDriver
from tools import flags

FLAGS = flags.FLAGS

class AddressManager():
    """Manages the address querys"""
    def __init__(self):
        self.driver = BuiltinDriver()

    # To do: add cache decorator
    # @CacheControl.cached(timeout=60, key_prefix='CACHE_ADDRESS')
    def handle_address(self, addr):
        try:
            print "handle_address: "+str(addr)
            addr_info = self.driver.request_address_info(addr)
            return addr_info

        except Exception, e:
            raise Exception("handle_address error: %s", e)   

if __name__ == '__main__':
    FLAGS(sys.argv)
    address = 'tm1q6jxakzk8xcfz0qazqsltft209s4gn3lgh3tlam'
    myManager = AddressManager()
    print myManager.handle_address(address)
