# coding: utf-8
from __future__ import unicode_literals


from seecode.libs.core.data import logger
from seecode.apps.node.models import HostInfo
from seecode.libs.units import close_old_connections
from seecode.libs.core.exceptions import ParameterIsEmptyException
from seecode.libs.core.exceptions import QueryConditionIsEmptyException


def create_host_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    hostname = kwargs.get('hostname', None)
    ipv4 = kwargs.get('ipv4', None)
    ipv6 = kwargs.get('ipv6', None)
    role = kwargs.get('role', 'client')
    ui_version = kwargs.get('ui_version', None)
    client_version = kwargs.get('client_version', None)

    if not all((hostname, role, )):
        raise ParameterIsEmptyException(u'"hostname, role" parameters cannot be empty !')

    close_old_connections()
    host = HostInfo(
        hostname=hostname,
        ipv4=ipv4,
    )
    if role and role.lower() == 'ui':
        host.is_role_ui = True
    else:
        host.is_role_client = True
    if ui_version:
        host.ui_version = ui_version.strip()
    if client_version:
        host.client_version = client_version.strip()
    host.save()
    return host


def create_or_update_host(**kwargs):
    """

    :param kwargs:
    :return:
    """
    result = False
    hostname = kwargs.get('hostname', None)
    ipv4 = kwargs.get('ipv4', None)
    ipv6 = kwargs.get('ipv6', None)
    role = kwargs.get('role', 'client')
    ui_version = kwargs.get('ui_version', '')
    client_version = kwargs.get('client_version', '')

    close_old_connections()

    try:
        sql_where = {}
        if ipv4:
            sql_where['ipv4'] = ipv4
        if ipv6:
            sql_where['ipv6'] = ipv6

        if not sql_where:
            raise QueryConditionIsEmptyException(u'Missing "ipv4, ipv6" key parameters!')

        item = HostInfo.objects.filter(**sql_where).first()
        if item:
            if hostname:
                item.hostname = hostname.strip()
            if ui_version:
                item.ui_version = ui_version.strip()
            if client_version:
                item.client_version = client_version.strip()
            item.save()
            result = True
        else:
            create_host_obj(**kwargs)
            result = True
    except HostInfo.DoesNotExist as ex:
        logger.warning(ex)
    return result
