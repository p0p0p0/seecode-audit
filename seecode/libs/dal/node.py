# coding: utf-8
from __future__ import unicode_literals

from django.core.cache import cache

from seecode.libs.core.data import logger
from seecode.apps.node.models import HostInfo
from seecode.libs.units import close_old_connections
from seecode.libs.core.exceptions import ParameterIsEmptyException
from seecode.libs.core.exceptions import QueryConditionIsEmptyException
from seecode.libs.core.cache_key import CONFIG_NODE_CACHE


def create_node_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    hostname = kwargs.get('hostname', None)
    ipv4 = kwargs.get('ipv4', None)
    ipv6 = kwargs.get('ipv6', None)

    if not all((hostname, ipv4, )):
        raise ParameterIsEmptyException(u'"hostname, ipv4" parameters cannot be empty !')

    close_old_connections()

    node = HostInfo(
        hostname=hostname,
        ipv4=ipv4,
        ipv6=ipv6
    )
    node.save()
    return node


def _get_node_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    result = None
    node_id = kwargs.get('node_id', None)
    hostname = kwargs.get('hostname', None)
    ipv4 = kwargs.get('ipv4', None)
    close_old_connections()

    try:
        sql_where = {}
        if node_id:
            sql_where['id'] = int(node_id)
        if hostname:
            sql_where['hostname'] = hostname
        if ipv4:
            sql_where['ipv4'] = ipv4

        if not sql_where:
            raise QueryConditionIsEmptyException(u'Missing "node_id, hostname" key parameters!')

        item = HostInfo.objects.get(**sql_where)
        result = item
    except HostInfo.DoesNotExist as ex:
        logger.warning(ex)
    return result


def get_node_by_id(node_id):
    """

    :param node_id:
    :return:
    """
    if node_id:
        cache_key = '{0}:{1}'.format(CONFIG_NODE_CACHE[1], node_id)
        cache_obj = cache.get(cache_key)
        if cache_obj:
            return cache_obj
    obj = _get_node_obj(node_id=node_id)
    if obj:
        cache.set(cache_key, obj, CONFIG_NODE_CACHE[0])
    return obj


def get_node_by_ip(ipv4):
    """

    :param ipv4:
    :return:
    """
    return _get_node_obj(ipv4=ipv4)


def get_node_by_hostname(hostname):
    """

    :param hostname:
    :return:
    """
    return _get_node_obj(hostname=hostname)
