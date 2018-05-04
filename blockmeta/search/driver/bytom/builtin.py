from blockmeta.utils.bytom import remove_0x
from flask import current_app
from flask import url_for
import re


ADDRESS_RE = re.compile('^bm[1-9A-HJ-NP-Za-km-z]{40}\\Z')
HEIGHT_RE = re.compile('(?:0|[1-9][0-9]*)\\Z')
LEN_64_RE = re.compile('[0-9a-fA-F]{0,64}\\Z')


class BuiltinDriver:
    @property
    def type(self):
        return 'builtin'

    def __init__(self):
        self.logger = current_app.logger

    def search(self, info):
        try:
            if HEIGHT_RE.match(info):
                found = self.search_block(int(info))
                return {'type': found['name'], 'value': found['uri']}

            if ADDRESS_RE.match(info):
                found = self.search_address(info)
                return {'type': found['name'], 'value': found['uri']}

            if LEN_64_RE.match(remove_0x(info)):
                found = self.search_block(info) or self.search_transaction(info)
                return {'type': found['name'], 'value': found['uri']}

            return None

        except Exception, e:
            self.logger.error("Search.bytom.BuiltinDriver.search Error: %s" % str(e))

    def search_block(self, key):
        value = url_for('block', block_id = key)
        return {
            'name': 'block',
            'uri': value
        }


    def search_address(self, address):
        value = url_for('address', address = address)
        return {
            'name': 'address'
            'uri': value
        }

    def search_transaction(self, tx_id):
        value = url_for('tx', tx_hash = tx_id)
        return {
            'name': 'tx'
            'uri': value
        }