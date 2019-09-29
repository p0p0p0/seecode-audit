# coding: utf-8
from __future__ import unicode_literals

from django.core.cache import cache

from seecode.libs.core.data import logger
from seecode.apps.node.models import HostServiceInfo
from seecode.libs.units import close_old_connections
from seecode.libs.core.exceptions import ParameterIsEmptyException
from seecode.libs.core.exceptions import QueryConditionIsEmptyException
from seecode.libs.core.cache_key import CONFIG_NODE_CACHE


def create_node_service_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    node_obj = kwargs.get('node_obj', None)
    service_obj = kwargs.get('service_obj', None)
    ppid = kwargs.get('ppid', None)
    pid = kwargs.get('pid', None)
    status = kwargs.get('status', None)

    if not all((node_obj, service_obj, ppid, pid)):
        raise ParameterIsEmptyException(u'"node_obj, service_obj, ppid, pid" parameters cannot be empty !')

    close_old_connections()

    node = HostServiceInfo(
        node=node_obj,
        service=service_obj,
        ppid=ppid,
        pid=pid,
        status=status,
    )
    node.save()
    return node


def _get_node_service_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    result = None
    pid = kwargs.get('pid', None)
    close_old_connections()

    try:
        sql_where = {}
        if pid:
            sql_where['pid'] = int(pid)

        if not sql_where:
            raise QueryConditionIsEmptyException(u'Missing "pid" key parameters!')

        item = HostServiceInfo.objects.get(**sql_where)
        result = item
    except HostServiceInfo.DoesNotExist as ex:
        logger.warning(ex)
    return result


def get_node_service_by_pid(pid):
    """

    :param pid:
    :return:
    """
    if pid:
        cache_key = '{0}:{1}'.format(CONFIG_NODE_CACHE[2], pid)
        cache_obj = cache.get(cache_key)
        if cache_obj:
            return cache_obj
    obj = _get_node_service_obj(pid=pid)
    if obj:
        cache.set(cache_key, obj, CONFIG_NODE_CACHE[0])
    return obj
