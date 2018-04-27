#! /usr/bin/env python
# -*- coding: utf-8 -*-

import re

HASH_PREFIX_RE = re.compile('[0-9a-fA-F]{0,64}\\Z')
HASH_PREFIX_MIN = 6


def is_hash_prefix(s):
    if s.startswith("0x"):
        s = s[2:]
    return HASH_PREFIX_RE.match(s) and len(s) >= HASH_PREFIX_MIN


def from_hex(x):
    return None if x is None else x.decode('hex')


hashin_hex  = from_hex


