# coding: utf-8
from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache

from seecode.libs.units import close_old_connections
from seecode.libs.core.cache_key import SYSTEM_CACHE


def get_permissions_by_all_module():
    """
    获取所有模块
    :return:
    """

    #if cache.get(SYSTEM_CACHE[3]):
    #    return cache.get(CACHE_KEY)

    result = {
        "sys": [],
        "project": [],
        "engine": [],
        "task": [],
        "node": [],
        "report": [],
    }
    """"

    """
    close_old_connections()
    result['sys'] = ContentType.objects.filter(id__in=[12, 13, 14, 15, 16, 21, 22, 23, 24 ,25,26])
    result['project'] = ContentType.objects.filter(id__in=[4, 5, 6, 7, 8])
    result['engine'] = ContentType.objects.filter(id__in=[17, 18, 19, 20])
    result['task'] = ContentType.objects.filter(id__in=[9, 10, 11, 1])
    result['node'] = ContentType.objects.filter(id__in=[2, 3])
    # result['report'] = ContentType.objects.filter(id__in=[18, 19, 20, 21])
    set_cache(result)
    return result


def set_cache(obj, timeout=60 * 60 * 24):
    """
    设置cache
    :param obj:
    :param timeout:
    :return:
    """
    try:
        if obj:
            cache.set(SYSTEM_CACHE[3], obj, timeout)
        return True
    except:
        return False


def delete_user_per_cache(user_id):
    """

    :param user_id:
    :return:
    """
    cache_key = '{0}:{1}'.format(SYSTEM_CACHE[3], user_id)
    cache.set(cache_key, None, 0)
