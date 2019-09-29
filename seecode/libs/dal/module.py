# coding: utf-8
from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.db.models import Q

from seecode.libs.core.log import logger
from seecode.libs.units import close_old_connections

CACHE_KEY = 'module_syslog'


def get_module_obj(**kwargs):
    """
    获取模块
    :param kwargs:
    :return:
    """
    module_id = kwargs.get('module_id', None)

    try:
        sql_where = {}
        if module_id:
            sql_where['id'] = int(module_id)

        close_old_connections()
        item = ContentType.objects.get(**sql_where)
        return item
    except ContentType.DoesNotExist as ex:
        logger.warn(ex)
        return None


def get_sys_module_obj():
    """
    获取日志模块
    :return:
    """
    try:
        cache_obj = cache.get(CACHE_KEY)
        if cache_obj:
            return cache_obj
        module_list = [
            # system
            1, 2, 3, 4, 5, 6, 13,
            # article
            10, 11, 12,
            # mobile
            28, 30, 32,
            # vuln
            19, 20, 21,
            # gitscan
            22, 23,
            # cve
            25,
        ]
        close_old_connections()
        item = ContentType.objects.filter(~Q(id__in=module_list))
        if item:
            cache.set(CACHE_KEY, item, 60 * 60*24)
        return item
    except ContentType.DoesNotExist as ex:
        logger.warn(ex)
        return None
