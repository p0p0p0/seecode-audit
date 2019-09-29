# coding: utf-8
from __future__ import unicode_literals

from django.core.cache import cache

from seecode.apps.node.models import UpgradeVersionInfo
from seecode.libs.dal.upgrade_changelog import create_changelog_obj
from seecode.libs.core.cache_key import UPGRADE_CACHE


def get_current_client_version():
    """
    获取客户端版本
    :return:
    """
    cached = cache.get(UPGRADE_CACHE[2])
    if cached:
        return cached
    obj = UpgradeVersionInfo.objects.filter(role=2).first()
    cache.set(UPGRADE_CACHE[2], obj, UPGRADE_CACHE[0])
    return obj


def update_client_major_version(**kwargs):
    """

    :return:
    """
    action = kwargs.get('action', None)
    module = kwargs.get('module', None)
    description = kwargs.get('description', None)
    create_changelog_obj(
        action=action,
        module=module,
        description=description,
    )
    result = False
    ver = get_current_client_version()
    if ver:
        ver.major += 1
        ver.minor = 0
        ver.revision = 0
        ver.save()
        result = True
        cache.set(UPGRADE_CACHE[2], None, 0)
    return result


def update_client_minor_version(**kwargs):
    """

    :return:
    """
    action = kwargs.get('action', None)
    module = kwargs.get('module', None)
    description = kwargs.get('description', None)
    create_changelog_obj(
        action=action,
        module=module,
        description=description,
    )
    result = False
    ver = get_current_client_version()
    if ver:
        ver.minor += 1
        ver.revision = 0
        ver.save()
        result = True
        cache.set(UPGRADE_CACHE[2], None, 0)
    return result


def update_client_revision_version(**kwargs):
    """

    :return:
    """
    action = kwargs.get('action', None)
    module = kwargs.get('module', None)
    description = kwargs.get('description', None)
    create_changelog_obj(
        action=action,
        module=module,
        description=description,
    )
    result = False
    ver = get_current_client_version()
    if ver:
        ver.revision += 1
        ver.save()
        result = True
        cache.set(UPGRADE_CACHE[2], None, 0)
    return result
