# coding: utf-8

from django import template
from django.core.cache import cache

from seecode.apps.tactic.models import VulnCategoryInfo

register = template.Library()


@register.filter(name='get_sub_list')
def get_sub_list(value):
    """
    :param value:
    :return:
    """
    if value:
        return VulnCategoryInfo.objects.filter(parent__id=value)
    else:
        return []
    

