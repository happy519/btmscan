#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import current_app
from flask.ext.restful import Resource, reqparse
from blockmeta import utils, flags
from blockmeta.tools.bytom import is_hash_prefix
from blockmeta.constant import DEFAULT_START, DEFAULT_OFFSET, DEFAULT_LIST

FLAGS = flags.FLAGS


class TxAPI(Resource):

    def __init__(self):
        manager = FLAGS.tx_manager
        self.manager = utils.import_object(manager)
        self.logger = current_app.logger

        self.parser = reqparse.RequestParser()
        self.parser.add_argument('detail', type=int, help='', ignore=True)
        self.parser.add_argument('chain', type=str, help='')
        super(TxAPI, self).__init__()

    def get(self, tx_hash):
        try:
            args = self.parser.parse_args()
            chain_type = args.get('chain')

            detail = 0 if not args.get('detail') else 1

            if tx_hash is None:
                raise Exception("void hash")

            # tx hash
            if not tx_hash.startswith("GENESIS") and not is_hash_prefix(tx_hash):
                raise Exception("Not a valid transaction hash")

            data = self.manager.handle_mempool_tx(tx_hash)
            if not data:
            data = self.manager.handle_tx(tx_hash, detail, chain_type)
            return utils.wrap_response(data=data)
        except Exception, e:
            self.logger.error("TxAPI.get Error: %s" % str(e))
            return utils.wrap_error_response("tx_error")


class TxListAPI(Resource):

    def __init__(self):
        self.logger = current_app.logger
        self.manager = utils.import_object(FLAGS.tx_manager)

        self.parser = reqparse.RequestParser()
        self.parser.add_argument('offset', type=int, help='block to')
        self.parser.add_argument('start', type=int, help='block from')
        self.parser.add_argument('chain', type=str, help='chain type')
        self.parser.add_argument('page', type=int, help='page number')

        super(TxListAPI, self).__init__()

    def get(self):
        try:
            args = self.parser.parse_args()
            start, offset = args.get('start'), args.get('offset')
            chain_type = args.get('chain')
            page = args.get('page')

            # return block in range [start, offset)
            if not isinstance(start, int):
                if isinstance(page, int):
                    start = DEFAULT_OFFSET * (page - 1)
                else:
                    start = DEFAULT_START

            if not isinstance(offset, int):
                if isinstance(page, int):
                    offset = DEFAULT_OFFSET * page
                else:
                    offset = DEFAULT_OFFSET

            result = self.manager.list_txs(start, offset, chain_type)
            result['no_page'] = 1 if not page else int(page)
            return utils.wrap_response(data=result)
        except Exception, e:
            self.logger.error("TxListAPI.get Error: %s" % str(e))
            return utils.wrap_error_response('tx_error')
