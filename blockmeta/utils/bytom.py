# -*- coding: utf-8 -*-
from relay import BYTOM_MINERS
import re

HASH_PREFIX_RE = re.compile('[0-9a-fA-F]{0,64}\\Z')
HASH_PREFIX_MIN = 6
BASE_SUBSIDY = 41250000000
SUBSIDY_REDUCTION_INTERVAL = 840000

def is_hash_prefix(s):
    ss = remove_0x(s)
    return HASH_PREFIX_RE.match(ss) and len(s) >= HASH_PREFIX_MIN


def remove_0x(s):
    return s[2:] if s.startswith("0x") else s


def format_bytom_neu(value):
    return long(value) / (10 ** 8)

def get_base_reward(hight):
    return BASE_SUBSIDY >> (hight/SUBSIDY_REDUCTION_INTERVAL)

def get_miner_addr(block):
    for tx in block['transactions']:
        if is_coinbase(tx):
            for tx_out in tx['outputs']:
                return tx_out['address'] if 'address' in tx_out else None

    raise Exception('No coinbase transaction in block %s', block['height'])


def is_coinbase(tx):
    for tx_in in tx['inputs']:
        if tx_in['type'] == 'coinbase':
            return True

    return False

def get_pool(addr):
    if not addr:
        return None

    for key, value in BYTOM_MINERS.items():
        if addr in value:
            return key

    return addr