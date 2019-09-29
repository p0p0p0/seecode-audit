# coding: utf-8
from __future__ import unicode_literals

from django.core.cache import cache

from seecode.libs.core.data import logger
from seecode.apps.node.models import ServiceInfo
from seecode.apps.node.models import HostInfo
from seecode.apps.node.models import HostServiceInfo
from seecode.libs.units import close_old_connections
from seecode.libs.core.exceptions import ParameterIsEmptyException
from seecode.libs.core.exceptions import QueryConditionIsEmptyException
from seecode.libs.core.cache_key import SYSTEM_CACHE


def create_service_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    name = kwargs.get('name', None)
    key = kwargs.get('key', None)
    role = kwargs.get('role', None)
    process_keyword = kwargs.get('process_keyword', None)
    description = kwargs.get('description', None)

    if not all((name, key, process_keyword, )):
        raise ParameterIsEmptyException(u'"name, key, process_keyword" parameters cannot be empty !')
    close_old_connections()

    service = ServiceInfo(
        name=name,
        key=key,
        process_keyword=process_keyword,
        description=description,
        role=role,
    )
    service.save()
    return service


def _get_service_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    result = None
    service_id = kwargs.get('service_id', None)
    key = kwargs.get('key', None)
    close_old_connections()

    try:
        sql_where = {}
        if service_id:
            sql_where['id'] = int(service_id)
        if key:
            sql_where['key'] = key

        if not sql_where:
            raise QueryConditionIsEmptyException(u'Missing "service_id, key" key parameters!')

        item = ServiceInfo.objects.get(**sql_where)
        result = item
    except ServiceInfo.DoesNotExist as ex:
        logger.warning(ex)
    return result


def get_service_by_id(app_id):
    """

    :param app_id:
    :return:
    """
    if app_id:
        cache_key = '{0}:{1}'.format(SYSTEM_CACHE[5], app_id)
        cache_obj = cache.get(cache_key)
        if cache_obj:
            return cache_obj
    obj = _get_service_obj(app_id=app_id)
    if obj:
        cache.set(cache_key, obj, SYSTEM_CACHE[0])
    return obj


def get_app_by_key(key):
    """

    :param key:
    :return:
    """
    if key:
        cache_key = '{0}:{1}'.format(SYSTEM_CACHE[6], key)
        cache_obj = cache.get(cache_key)
        if cache_obj:
            return cache_obj
    obj = _get_service_obj(key=key)
    if obj:
        cache.set(cache_key, obj, SYSTEM_CACHE[0])
    return obj


def create_or_update_hostservice(**kwargs):
    """

    :param kwargs:
    :return:
    """
    result = False

    ipv4 = kwargs.get('ipv4', None)
    key = kwargs.get('key', None)
    ppid = kwargs.get('ppid', None)
    pid = kwargs.get('pid', None)
    status = kwargs.get('status', None)

    if not all((ipv4, key)):
        raise QueryConditionIsEmptyException(u'Missing "ipv4, key" key parameters!')
    close_old_connections()
    try:
        host = HostInfo.objects.filter(ipv4=ipv4).first()
        service = ServiceInfo.objects.filter(key=key).first()

        if host and service:
            host_service = HostServiceInfo.objects.filter(host_id=host.id, service_id=service.id).first()
            if host_service:
                host_service.status = status
                host_service.ppid = ppid
                host_service.pid = pid
                host_service.save()
                result = True
            else:
                host_service = HostServiceInfo(
                    host=host,
                    service=service,
                    status=status,
                    ppid=ppid,
                    pid=pid,
                )
                host_service.save()
                result = True
    except Exception as ex:
        import traceback;traceback.print_exc()
        logger.warning(ex)
    return result


def delete_app_list(id_list):
    """

    :param id_list:
    :return:
    """
    if id_list:
        app_list = ServiceInfo.objects.filter(id__in=id_list)
        for item in app_list:
            cache_key = '{0}:{1}'.format(SYSTEM_CACHE[5], item.id)
            cache.set(cache_key, None, 0)
            item.delete()
