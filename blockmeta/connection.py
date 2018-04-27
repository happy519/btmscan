#! /usr/bin/env python
# -*- coding: utf-8 -*-


import time
from blockmeta import flags
from blockmeta.cache_module import MongodbClient

FLAGS = flags.FLAGS


def init_mongodb(app):
    if FLAGS.MONGODB_ENABLE:
        app.mongodb_btm = MongodbClient(host=FLAGS.mongo_btm_host, port=FLAGS.mongo_btm_port)

    else:
        app.mongodb_btm = None

