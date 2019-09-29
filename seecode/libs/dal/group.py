# coding: utf-8
from __future__ import unicode_literals

from django.contrib.auth.models import Group

from seecode.libs.core.log import logger
from seecode.libs.units import close_old_connections
from seecode.libs.dal.config import get_config


def get_group_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    group_id = kwargs.get('group_id', None)
    close_old_connections()

    try:
        sql_where = {}
        if group_id:
            sql_where['id'] = int(group_id)

        item = Group.objects.get(**sql_where)
        return item
    except Group.DoesNotExist as ex:
        logger.warn(ex)
        return None


def is_association_settings(group_id):
    """

    :param group_id:
    :return:
    """
    result = False
    if group_id:
        conf = get_config()

        if group_id == conf['port']['ops_group'] or group_id == conf['port']['sec_group']:
            result = True
        elif group_id == conf['soft']['ops_group'] or group_id == conf['soft']['sec_group']:
            result = True
        elif group_id == conf['test']['sec_group']:
            result = True
        elif group_id == conf['vuln']['sec_group']:
            result = True

    return result


