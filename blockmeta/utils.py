#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import random
import datetime
import uuid
import re
from time import time, mktime
import StringIO
from PIL import Image
from flask.globals import current_app
from flask import request, g

try:
    from werkzeug.wsgi import wrap_file
except ImportError:
    from werkzeug.utils import wrap_file
from werkzeug.datastructures import Headers
from flask.ext.uploads import extension

TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

ERROR_MSG = {
    'zh': {
        'market_error': '市场数据无法获得',
        'tx_error': '交易信息查询失败',
        'block_error': '区块信息查询失败',
        'block_notfound': '区块信息不存在',
        'address_error': '地址信息查询失败',
        'stat_error': '统计数据获取失败',
        'chart_error': '图表数据获取失败',
        'search_notfound': '搜索结果不存在',
        'search_error': '获取搜索结果失败',
        'archive_error': '档案数据获取失败',
        'archive_submit_error': '档案信息上传失败',
        'qr_error': '无法产生二维码',
        'logo_error': '无法产生验证码',
        'miner_error': '无法获得矿工信息',
        'node_error': '节点信息获取失败',

    },
    'en': {
        'market_error': 'Oops! Cannot Obtain Market Data',
        'tx_error': 'Invalid Transaction Information',
        'block_error': 'Invalid Block Information',
        'block_notfound': 'No Block Information Found',
        'address_error': 'Invalid Address Information',
        'stat_error': 'Invalid Statistics',
        'chart_error': 'Invalid Chart Data',
        'search_notfound': 'No Pattern Found',
        'search_error': 'Oops! Search Error!',
        'about_error': 'No Related Docs Found',
        'archive_error': 'Invalid Archive Information',
        'archive_submit_error': 'Invalid Data. Cannot Submit Archive',
        'qr_error': 'Cannot Generate QR Code',
        'logo_error': 'Cannot Generate Captcha Image',
        'miner_error': 'Invaild Miner Information',
        'node_error': 'No Nodes Information',

    }
}


def generate_uid(topic, size=16):
    characters = '01234567890abcdefghijklmnopqrstuvwxyz'
    choices = [random.choice(characters) for x in xrange(size)]
    return '%s-%s' % (topic, ''.join(choices))


def import_class(import_str):
    """Returns a class from a string including module and class"""
    mod_str, _sep, class_str = import_str.rpartition('.')
    try:
        __import__(mod_str)
        return getattr(sys.modules[mod_str], class_str)
    except Exception, e:
        print e
        # logging.debug(_('Inner Exception: %s'), exc)
        # raise exception.NotFound(_('Class %s cannot be found') % class_str)


def import_object(import_str, *args, **kwargs):
    """Returns an object including a module or module and class"""
    if isinstance(import_str, str):
        try:
            __import__(import_str)
            return sys.modules[import_str]
        except ImportError:
            cls = import_class(import_str)
            return cls()
    elif isinstance(import_str, list):
        modules = []
        for s in import_str:
            try:
                __import__(s)
                modules.append(sys.modules[s])
            except ImportError:
                cls = import_class(s)
                modules.append(cls())
        return modules


def import_driver(drivers):
    driver_dict = {}
    for dpath in drivers:
        proj, pkg, _, type, _, _ = dpath.split('.')
        driver_dict[type] = import_object(dpath)
    return driver_dict


def mk_timestamp(now):
    return int(mktime(now.timetuple()))


def next_month(now):
    if now.month == 12:
        nextmonth = now.replace(year=now.year + 1, month=1, day=1, hour=0, minute=0, second=0)
    else:
        nextmonth = now.replace(month=now.month + 1, day=1, hour=0, minute=0, second=0)
    return nextmonth


def next_week(now):
    next_week = now + datetime.timedelta(days=7)
    return next_week


def last_day(now):
    last_day = now - datetime.timedelta(days=1)
    return int(mktime(last_day.timetuple()))


def next_day(now):
    next_day = now + datetime.timedelta(days=1)
    return next_day


def last_hour(now):
    this_hour = now.replace(minute=0, second=0)
    last_hour = this_hour - datetime.timedelta(hours=1)
    return int(mktime(last_hour.timetuple()))


def next_hour(now):
    this_hour = now.replace(minute=0, second=0)
    next_hour = this_hour + datetime.timedelta(hours=1)
    return next_hour


def this_hour(now):
    this_hour = now.replace(minute=0, second=0)
    return int(mktime(this_hour.timetuple()))


def total_seconds(td):
    if hasattr(td, 'total_seconds'):
        return td.total_seconds()
    else:
        return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10 ** 6) / 10 ** 6


def wrap_response(data='', status='success', code='200', message='', **kwargs):
    return dict(status=status, data=data, code=code, message=message)


def wrap_error_response(message='', data='', status='failure', code='500'):
    lang = g.lang if g.get('lang', None) else 'zh'
    response = ERROR_MSG[lang][message]
    print response
    return dict(status=status, data=data, code=code, message=response)


def wrap_validate_response(message=u'存在错误', errors='', status='error', code='200'):
    """ 返回错误 """
    return dict(message=message, errors=errors, status=status, code=code)


def form_errors(form):
    """
    返回form错误
    :param form: form
    :return:
    """
    error_list = ''
    for key in form.errors.keys():
        d = {
            'field': key,
            'message': form.errors[key][0]
        }
        error_list += '%s ' % d['message']
    return error_list, False


def random_filename():
    return str(uuid.uuid4())


def int_round(x):
    return int(round(x))


def save_evidence(evidence, file_name):
    from blockmeta.extension import evidences
    ext = extension(file_name)
    filename = '%s.%s' % (random_filename(), ext)
    folder = evidences.config.destination
    filename = evidences.resolve_conflict(folder, filename)
    path = os.path.join(folder, filename)
    evidence.save("%s.jpeg" % path)
    return filename
