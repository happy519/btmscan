# -*- coding: utf-8 -*-
import pickle
import hashlib
from functools import wraps
from flask import request, json, current_app as app
from blockmeta import flags

FLAGS = flags.FLAGS


class CacheControl(object):

    @classmethod
    def set_cache(cls, key, data, expire):
        """
        设置缓存
        :param key:
        :param data:
        :param expire:
        :return:
        """
        try:
            cache_data = pickle.dumps(data)
        except pickle.PickleError:
            return False
        if not app.cache:
            return False
        app.cache.set_and_expire(key, cache_data, expire)
        return True

    @classmethod
    def get_cache(cls, key):
        if not app.cache:
            return None
        data = app.cache.get(key)
        if data:
            try:
                result = pickle.loads(data)
                return result
            except pickle.UnpicklingError:
                return data
        return None

    @classmethod
    def cached(cls, timeout=600, key_prefix=None):
        """
        缓存番薯
        :param timeout:
        :param key_prefix:
        :return:
        """

        def _cached(func):
            @wraps(func)
            def wrapper(*args, **kwargs):

                cache_key = cls._make_key_prefix()
                if key_prefix:
                    cache_key = '{0}-{1}'.format(key_prefix, cache_key)
                cache = cls.get_cache(cache_key)
                if cache and FLAGS.CACHE_ENABLE:
                    return cache
                func_result = func(*args, **kwargs)
                cls.set_cache(cache_key, func_result, expire=timeout)
                return func_result

            return wrapper

        return _cached

    @classmethod
    def _make_key_prefix(cls):
        key = str(request.method) + str(request.path) + str(request.args)
        cache_key = hashlib.md5(key.encode()).hexdigest()
        return cache_key
