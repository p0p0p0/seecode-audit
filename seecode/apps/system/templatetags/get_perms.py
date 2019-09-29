# coding: utf-8

from django import template
from django.core.cache import cache

from django.contrib.auth.models import User, Group, Permission

register = template.Library()


@register.filter(name='get_perms')
def get_perms(value):
    """
    :param value:
    :return:
    """

    perms = Permission.objects.filter(content_type__id=value)

    return perms
