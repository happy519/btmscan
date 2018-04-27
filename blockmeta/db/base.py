#! /usr/bin/env python

"""
Base class for classes that need modular database access.
"""

from blockmeta import flags
from blockmeta import utils

FLAGS = flags.FLAGS


class Base(object):
    """DB driver is injected in the init method"""

    def __init__(self, db_driver=None):
        if not db_driver:
            db_driver = FLAGS.db_driver
        self.db = utils.import_object(db_driver)
