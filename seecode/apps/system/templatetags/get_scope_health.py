# coding: utf-8

from django import template

register = template.Library()


@register.filter(name='get_scope_health')
def get_scope_health(value):
    """
    :param value:
    :return:
    """
    if value:
        if isinstance(value, float):
            return str(int(value))[1:]
        return str(value)[1:]
