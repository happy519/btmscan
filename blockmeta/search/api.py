from flask.ext.restful import Resource, reqparse
from flask import current_app

from blockmeta.utils import util
from tools import flags
from manager import BlockManager
from blockmeta.constant import DEFAULT_OFFSET, DEFAULT_START

FLAGS = flags.FLAGS

class SearchAPI(Resource):
    
    def __init__(self):
        manager =  FLAGS.search_manager
        self.manager = utils.import_object(manager)
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('q', type=str, help='query info', ignore=False)
        self.logger = current_app.logger
        super(SearchAPI, self).__init__()
    
    
    def post(self):
        found = None
        args = self.parser.parse_args()
        info = args.get('q')

        try:
            found = self.manager.search(info, chain_type)  # return {'type': found['name'], 'value': found['uri']} 
            assert found
            return utils.wrap_response(status='success', data=found, code='302')
        except Exception, e:
            self.logger.debug("SEARCH: %s" % str(e))
            return utils.wrap_error_response('search_notfound')
    