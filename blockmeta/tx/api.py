#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask.ext.restful import Resource, reqparse
from flask import current_app

from tools import flags
from blockmeta.utils.bytom import is_hash_prefix
from blockmeta.utils import util
from manager import TxManager
from blockmeta.constant import DEFAULT_OFFSET, DEFAULT_START

FLAGS = flags.FLAGS


class TxAPI(Resource):

    def __init__(self):
        self.logger = current_app.logger
        self.manager = TxManager()
        super(TxAPI, self).__init__()

    def get(self, tx_hash):
        try:
            if not is_hash_prefix(tx_hash):
                raise Exception("Transaction hash is wrong!")

            result = self.manager.handle_tx(tx_hash) if tx_hash else {}
            return result
        except Exception, e:
            self.logger.error("TxAPI.get Error: %s" % str(e))
            util.wrap_error_response("tx_error")


class TxListAPI(Resource):

    def __init__(self):
        self.logger = current_app.logger
        self.manager = TxManager()

        self.parser = reqparse.RequestParser()
        self.parser.add_argument('offset', type=int, help='block to')
        self.parser.add_argument('start', type=int, help='block from')
        self.parser.add_argument('page', type=int, help='page number')

        super(TxListAPI, self).__init__()

    def get(self):
        try:
            args = self.parser.parse_args()
            start, offset = args.get('start'), args.get('offset')
            page = args.get('page')

            # return block in range [start, offset)
            if not isinstance(start, int):
                if isinstance(page, int):
                    start = DEFAULT_OFFSET * (page-1)
                else:
                    start = DEFAULT_START

            if not isinstance(offset, int):
                if isinstance(page, int):
                    offset = DEFAULT_OFFSET * page
                else:
                    offset = DEFAULT_OFFSET

            result = self.manager.list_txs(start, offset)
            result['no_page'] = 1 if not page else int(page)
            return util.wrap_response(data=result)
        except Exception, e:
            self.logger.error("TxListAPI.get Error: %s" % str(e))
            return util.wrap_error_response('tx_error')
