# coding: utf-8
from __future__ import unicode_literals

from django.core.cache import cache

from seecode.libs.core.data import logger
from seecode.apps.system.models import LanguageInfo
from seecode.libs.units import close_old_connections
from seecode.libs.core.exceptions import ParameterIsEmptyException
from seecode.libs.core.exceptions import QueryConditionIsEmptyException
from seecode.libs.core.cache_key import CONFIG_LANG_CACHE


def create_lang_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    name = kwargs.get('name', None)
    key = kwargs.get('key', None)

    if not name:
        raise ParameterIsEmptyException(u'Language name cannot be empty!')

    if name and len(name) > 16:
        name = name[:16]

    if not key:
        key = name.lower()
    else:
        key = key.lower()

    close_old_connections()

    lang = LanguageInfo(
        name=name,
        key=key,
    )
    lang.save()
    cache.set(CONFIG_LANG_CACHE[2], None, 0)
    return lang


def _get_lang_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    result = None
    lang_id = kwargs.get('lang_id', None)
    name = kwargs.get('name', None)
    key = kwargs.get('key', None)
    close_old_connections()

    try:
        sql_where = {}
        if name:
            sql_where['name__iexact'] = name.strip()
        if key:
            sql_where['key'] = key.lower()
        if lang_id:
            sql_where['id'] = int(lang_id)
        if not sql_where:
            raise QueryConditionIsEmptyException(u'Missing "lang_id, name, key" key parameters!')
        item = LanguageInfo.objects.get(**sql_where)
        result = item
    except LanguageInfo.DoesNotExist as ex:
        logger.warning(ex)
    return result


def get_lang_by_id(lang_id):
    """

    :param lang_id:
    :return:
    """
    if lang_id:
        cache_key = '{0}:{1}'.format(CONFIG_LANG_CACHE[1], lang_id)
        cache_obj = cache.get(cache_key)
        if cache_obj:
            return cache_obj
    obj = _get_lang_obj(lang_id=lang_id)
    if obj:
        cache.set(cache_key, obj, CONFIG_LANG_CACHE[0])
    return obj

def get_lang_by_name(name):
    """

    :param name:
    :return:
    """
    return _get_lang_obj(name=name)

def get_lang_by_key(key):
    """

    :param key:
    :return:
    """
    return _get_lang_obj(key=key)

def get_lang_all():
    """

    :return:
    """
    cache_obj = cache.get(CONFIG_LANG_CACHE[2])
    if cache_obj:
        return cache_obj
    obj = LanguageInfo.objects.all()
    if obj:
        cache.set(CONFIG_LANG_CACHE[2], obj, CONFIG_LANG_CACHE[0])
    return obj
