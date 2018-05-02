#! /usr/bin/env python
# -*- coding: utf-8 -*-


from driver.bytom.builtin import BuiltinDriver
from tools import flags

FLAGS = flags.FLAGS


class AddressManager:
    """Manages the address querys"""
    def __init__(self):
        self.driver = BuiltinDriver()

    def handle_address(self, addr):
        try:
            addr_info = self.driver.request_address_info(addr)
            return addr_info

        except Exception, e:
            raise Exception("handle_address error: %s", e)
