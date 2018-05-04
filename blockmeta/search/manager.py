from flask import current_app

from blockmeta.constant import DEFAULT_OFFSET
from driver.bytom.builtin import BuiltinDriver
from tools import flags

FLAGS = flags.FLAGS

class SearchManager(manager.Manager):
    """Manages the block querys"""
    def __init__(self, search_driver = None, *args, **kwargs):
        if not search_driver:
            search_driver = FLAGS.search_driver
        self.driver= utils.import_driver(search_driver)
        self.logger = current_app.logger
        super(SearchManager, self).__init__(*args, **kwargs)

    def search(self, query, chain_type):
        result = None
        try:
            result = self.driver[chain_type].search(query)
            return result

        except Exception, e:
            self.logger.error("SearchManager.search Error: %s" % str(e))
            raise Exception("search error: %s", e)
    