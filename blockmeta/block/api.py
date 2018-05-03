# -*- coding: utf-8 -*-

from flask.ext.restful import Resource, reqparse
from flask import current_app

from blockmeta.utils import util
from tools import flags
from manager import BlockManager
from blockmeta.constant import DEFAULT_OFFSET, DEFAULT_START

FLAGS = flags.FLAGS


class BlockAPI(Resource):
    def __init__(self):
        self.logger = current_app.logger
        self.manager = BlockManager()

        super(BlockAPI, self).__init__()

    def get(self, block_id):
        try:
            result = self.manager.handle_block(block_id)
            return util.wrap_response(result)
        except Exception, e:
            self.logger.error("BlockAPI.get Error: %s" % str(e))
            return util.wrap_error_response('block_error')


class BlockListAPI(Resource):

    def __init__(self):
        self.logger = current_app.logger
        self.manager = BlockManager()

        self.parser = reqparse.RequestParser()
        self.parser.add_argument('end', type=int, help='block to')
        self.parser.add_argument('start', type=int, help='block from')
        self.parser.add_argument('page', type=int, help='page number')

        super(BlockListAPI, self).__init__()

    def get(self):
        try:
            args = self.parser.parse_args()
            # start, end
            start, end = args.get('start'), args.get('end')
            page = args.get('page')

            # return block in range [start, end)
            if not isinstance(start, int):
                if isinstance(page, int):
                    start = DEFAULT_OFFSET * (page - 1)
                else:
                    start = DEFAULT_START

            if not isinstance(end, int):
                if isinstance(page, int):
                    end = DEFAULT_OFFSET * page
                else:
                    end = DEFAULT_OFFSET

            result = self.manager.list_blocks(start, end)
            result['page'] = 1 if not page else int(page)

            return util.wrap_response(data=result)
        except Exception, e:
            self.logger.error("BlockListAPI.get Error: %s" % str(e))
            return util.wrap_error_response('block_error')

