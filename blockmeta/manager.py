#! /usr/bin/env python
# -*- coding: utf-8 -*-


from blockmeta import flags
from blockmeta.db import base

FLAGS = flags.FLAGS


class Manager(base.Base):
    def __init__(self, db_driver=None):
        super(Manager, self).__init__(db_driver)
