# coding: utf-8
from __future__ import unicode_literals

from seecode.libs.core.log import logger
from seecode.apps.system.models import SyslogInfo
from seecode.libs.units import close_old_connections
from seecode.libs.dal.module import get_module_obj
from seecode.libs.core.common import get_localhost_ip
from seecode.libs.core.enum import LOG_LEVEL


def create_syslog_obj(**kwargs):
    """
    获取资产
    :param kwargs:
    :return:
    """
    title = kwargs.get('title', None)
    description = kwargs.get('description', None)
    stack_trace = kwargs.get('stack_trace', None)
    module = kwargs.get('module_id', None)
    object_id = kwargs.get('object_id', None)
    ipv4 = kwargs.get('ipv4', get_localhost_ip())
    sys_type = kwargs.get('type', 1)
    level = kwargs.get('level', LOG_LEVEL.INFO)
    try:

        if sys_type:
            sys_type = int(sys_type)
        if level:
            level = int(level)
        if module:
            module = get_module_obj(module_id=int(module))

        close_old_connections()
        log = SyslogInfo(
            title=title,
            description=description,
            stack_trace=stack_trace,
            module=module,
            object_id=object_id,
            ipv4=ipv4,
            type=sys_type,
            level=level,
        )
        log.save()

        return log
    except Exception as ex:
        logger.error(ex)
