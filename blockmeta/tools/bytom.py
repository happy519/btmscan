#! /usr/bin/env python
# -*- coding: utf-8 -*-

import re

HASH_PREFIX_RE = re.compile('[0-9a-fA-F]{0,64}\\Z')
HASH_PREFIX_MIN = 6


def is_hash_prefix(s):
    ss = remove_0x(s)
    return HASH_PREFIX_RE.match(ss) and len(s) >= HASH_PREFIX_MIN


def remove_0x(s):
    if s.startswith("0x"):
        s = s[2:]
    return s


def format_bytom_neu(value):
    btm = long(value) / (10 ** 8)
    return btm
