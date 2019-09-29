# coding: utf-8

from django import template
from django.core.cache import cache

from seecode.apps.node.models import HostServiceInfo

register = template.Library()


@register.filter(name='get_services')
def get_services(value):
    """
    :param value:
    :return:
    """
    if value:
        # TODO 添加 1 分钟cache
        return HostServiceInfo.objects.filter(host_id=value)
    else:
        return []
    

