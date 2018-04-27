#! /usr/bin/env python


from flask import current_app
from mongo import MongodbClient
from tools import flags
from tools import exception

FLAGS = flags.FLAGS
LOG =current_app.logger



