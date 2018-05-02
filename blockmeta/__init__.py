# -*- coding: ytf-8 -*-

from flask import Flask
from blockmeta import log, urls

DEFAULT_APP_NAME = 'btmscan'


def configure_modules(app):
    urls.register_api(app)


def configure_logging(app):
    log.init_log(app)


def create_app():
    app = Flask(DEFAULT_APP_NAME, static_folder='static', static_url_path='')
    # register log
    configure_logging(app)
    # register rest url
    configure_modules(app)

    return app


app = create_app()
