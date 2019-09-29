# coding: utf-8
from __future__ import unicode_literals

import ast

from django.core.cache import cache

from seecode.apps.system.models import ConfigInfo
from seecode.libs.core.cache_key import SYSTEM_CACHE
from seecode.libs.core.exceptions import QueryConditionIsEmptyException
from seecode.libs.core.log import logger
from seecode.libs.units import close_old_connections


def _get_config_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    config_id = kwargs.get('config_id', None)
    site = kwargs.get('site', None)
    close_old_connections()
    sql_where = {}

    if site:
        sql_where['site'] = site.strip()
    if config_id:
        sql_where['id'] = int(config_id)
    if not sql_where:
        raise QueryConditionIsEmptyException(u'Missing "config_id, site" key parameters!')

    try:
        item = ConfigInfo.objects.get(**sql_where)
        return item
    except ConfigInfo.DoesNotExist as ex:
        logger.warn('{0}, detail:{1}'.format(ex, sql_where))
        return None


def update_config_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    config_id = kwargs.get('config_id', None)
    site = kwargs.get('site', None)
    content = kwargs.get('content', None)

    close_old_connections()

    try:
        sql_where = {}
        if config_id:
            sql_where['id'] = int(config_id)

        item = ConfigInfo.objects.get(**sql_where)
        if item:
            if site:
                item.site = site
            item.content = content

            item.save()
            cache.set('{0}'.format(SYSTEM_CACHE[1]), None, 0)
            logger.debug('Update "{0}" config successfully.'.format(item.site))
        return item
    except ConfigInfo.DoesNotExist as ex:
        logger.warn(ex)
        return None


def get_config():
    """
    :return:
    """

    conf = None
    cache_obj = cache.get(SYSTEM_CACHE[1])
    if cache_obj:
        return cache_obj
    obj = _get_config_obj(config_id=1)

    if obj:
        conf = ast.literal_eval(obj.content)
        cache.set(SYSTEM_CACHE[1], conf, SYSTEM_CACHE[0])
    return conf
