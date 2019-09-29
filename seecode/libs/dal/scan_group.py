# coding: utf-8
from __future__ import unicode_literals

from django.core.cache import cache

from seecode.apps.scan.models import TaskGroupInfo
from seecode.libs.core.log import logger
from seecode.libs.units import close_old_connections
from seecode.libs.core.exceptions import ParameterIsEmptyException
from seecode.libs.core.exceptions import QueryConditionIsEmptyException
from seecode.libs.core.cache_key import SCAN_CACHE


def create_t_group_obj(**kwargs):
    """
    :param kwargs:
    :return:
    """
    profile_obj = kwargs.get('profile_obj', None)
    periodic_obj = kwargs.get('periodic_obj', None)
    sched_obj = kwargs.get('sched_obj', None)
    is_default = kwargs.get('is_default', False)
    name = kwargs.get('name', '')
    branch = kwargs.get('branch', '')
    args = kwargs.get('args', '')

    if not all((name, )):
        raise ParameterIsEmptyException(u'"name" parameters cannot be empty !')

    if name and len(name)>255:
        name = name[:255]

    close_old_connections()

    grp = TaskGroupInfo(
        profile=profile_obj,
        periodic=periodic_obj,
        sched=sched_obj,
        name=name.strip(),
        branch=branch,
        is_default=is_default,
        args=args.strip()
    )
    grp.save()

    return grp


def update_t_group_obj(**kwargs):
    """
    :param kwargs:
    :return:
    """
    group_id = kwargs.get('group_id', None)
    name = kwargs.get('name', None)
    profile_obj = kwargs.get('profile_obj', None)
    is_default = kwargs.get('is_default', False)

    close_old_connections()
    grp = TaskGroupInfo.objects.filter(id=group_id).first()
    if grp:
        if name:
            grp.name = name.strip()
        if profile_obj:
            grp.profile = profile_obj
        if is_default:
            TaskGroupInfo.objects.filter().update(is_default=False)
            grp.is_default = True
            cache.set(SCAN_CACHE[5], None, 0)
        grp.save()
    cache.set('{0}:{1}'.format(SCAN_CACHE[1], group_id), None, 0)

    return grp


def _get_t_group_obj(**kwargs):
    """
    获取资产
    :param kwargs:
    :return:
    """
    group_id = kwargs.get('group_id', None)
    name = kwargs.get('name', None)
    close_old_connections()

    try:
        sql_where = {}
        if group_id:
            sql_where['id'] = int(group_id)
        if name:
            sql_where['name'] = name.strip()
        if not sql_where:
            raise QueryConditionIsEmptyException(u'Missing "group_id, name" key parameters!')
        item = TaskGroupInfo.objects.get(**sql_where)
        return item
    except TaskGroupInfo.DoesNotExist as ex:
        logger.warn(ex)
        return None


def get_t_group_by_id(group_id):
    """

    :param group_id:
    :return:
    """

    cache_key = '{0}:{1}'.format(SCAN_CACHE[1], group_id)
    cache_obj = cache.get(cache_key)
    if cache_obj:
        return cache_obj
    obj = _get_t_group_obj(group_id=group_id)
    if obj:
        cache.set(cache_key, obj, SCAN_CACHE[0])
    return obj


def get_t_group_by_name(name):
    """

    :param name:
    :return:
    """
    return _get_t_group_obj(name=name)


def get_default_group():
    """

    :return:
    """
    cache_obj = cache.get(SCAN_CACHE[5])
    if cache_obj:
        return cache_obj
    obj = TaskGroupInfo.objects.filter(is_default=True).first()
    if obj:
        cache.set(SCAN_CACHE[5], obj, SCAN_CACHE[0])
    return obj


def get_all_group():
    """

    :return:
    """
    cache_obj = cache.get(SCAN_CACHE[2])
    if cache_obj:
        return cache_obj

    obj = TaskGroupInfo.objects.filter()
    if obj:
        cache.set(SCAN_CACHE[2], obj, 60*15)
    return obj


def delete_t_by_list(t_list):
    """

    :return:
    """
    group_list = TaskGroupInfo.objects.filter(id__in=t_list)
    for item in group_list:
        cache_key = '{0}:{1}'.format(SCAN_CACHE[1], item.id)
        cache.set(cache_key, None, 0)
        if item.periodic:
            item.periodic.delete()
    # TODO 检测是否有任务在执行
    TaskGroupInfo.objects.filter(id__in=t_list).delete()
    cache.set(SCAN_CACHE[2], None, 0)
