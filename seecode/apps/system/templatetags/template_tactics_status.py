# coding: utf-8

from django import template
from django.core.cache import cache

from seecode.apps.scan.models import ScanProfileInfo
from seecode.libs.dal.scan_profile import get_profile_by_id

register = template.Library()


@register.filter(name='template_tactics_status')
def template_tactics_status(value, profile_id):
    """
    :param value:
    :param profile_id:
    :return:
    """
    if value and profile_id:
        profile = get_profile_by_id(profile_id=profile_id)
        if profile.tactics.filter(id=value).exists():
            return True
        else:
            return False
    else:
        return False
    

