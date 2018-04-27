#! /usr/bin/env python


from flask import current_app
from blockmeta import exception
from mongo import MongodbClient
from blockmeta import flags

FLAGS = flags.FLAGS
LOG =current_app.logger


def get_mongo_cli():
    mongo_cli = MongodbClient(host=FLAGS.mongo_bytom_host, port=FLAGS.mongo_bytom_port)
    mongo_cli.use_db(FLAGS.mongo_bytom)
    return mongo_cli


def get_tx_by_hash(txhash):
    try:
        db = get_mongo_cli()
        tx = db.get_one(table=FLAGS.transaction_info, cond={FLAGS.tx_id: txhash})
    except Exception, e:
        LOG.debug("get_tx_by_hash: %s" % str(e))
        raise exception.DBError(e)
    return tx


def select_txin_by_hash(txhash):
    try:
        db = get_mongo_cli()
        tx = db.get_one(table=FLAGS.transaction_info, cond={FLAGS.tx_id: txhash})
        txin = tx.get[FLAGS.transaction_in]
    except Exception, e:
        LOG.debug("select_txin_by_hash: %s" % str(e))
        raise exception.DBError(e)
    return txin


def select_txout_by_id(txout_id):
    try:
        db = get_mongo_cli()
        txout = db.get_one(table=FLAGS.transaction_info, cond={FLAGS.txout_id: txout_id})
    except Exception, e:
        LOG.debug("select_txout_by_id: %s" % str(e))
        raise exception.DBError(e)
    return txout


def select_txout_by_hash(txhash):
    try:
        db = get_mongo_cli()
        tx = db.get_one(table=FLAGS.transaction_info, cond={FLAGS.tx_id: txhash})
        txouts = tx.get[FLAGS.transaction_out]
    except Exception, e:
        LOG.debug("select_txout_by_hash: %s" % str(e))
        raise exception.DBError(e)
    return txouts
