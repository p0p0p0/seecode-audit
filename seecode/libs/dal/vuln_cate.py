# coding: utf-8
from __future__ import unicode_literals

from django.core.cache import cache

from seecode.libs.core.data import logger
from seecode.apps.tactic.models import VulnCategoryInfo
from seecode.apps.system.models import TagInfo
from seecode.libs.units import close_old_connections
from seecode.libs.core.exceptions import ParameterIsEmptyException
from seecode.libs.core.exceptions import QueryConditionIsEmptyException
from seecode.libs.core.cache_key import VULN_CACHE


def create_cate_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    name = kwargs.get('name', None)
    key = kwargs.get('key', None)
    tag = kwargs.get('tag', None)
    parent = kwargs.get('parent', None)

    if not all((name, )):
        raise ParameterIsEmptyException(u'"name" parameters cannot be empty !')

    if name and len(name)>64:
        name = name[:64]

    close_old_connections()
    
    if parent and parent != "0":
        parent = VulnCategoryInfo.objects.filter(id=parent).first()

    cate = VulnCategoryInfo(
        name=name,
        key=key,
        tag=tag,
    )
    cate.save()
    if parent and parent != "0":
        cate.parent = parent
        cate.save()
    return cate


def _get_cate_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    result = None
    cate_id = kwargs.get('cate_id', None)
    name = kwargs.get('name', None)
    close_old_connections()

    try:

        sql_where = {}

        if cate_id:
            sql_where['id'] = int(cate_id)
        if name:
            sql_where['name'] = name
        if not sql_where:
            raise QueryConditionIsEmptyException(u'Missing "cate_id" key parameters!')

        item = VulnCategoryInfo.objects.get(**sql_where)
        result = item
    except VulnCategoryInfo.DoesNotExist as ex:
        logger.warning(ex)
    return result


def update_cate_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    result = None
    cate_id = kwargs.get('cate_id', None)
    name = kwargs.get('name', None)
    parent = kwargs.get('parent', None)
    key = kwargs.get('key', None)
    tag = kwargs.get('tag', None)

    try:
        sql_where = {}
        if cate_id:
            sql_where['id'] = int(cate_id)
        if not sql_where:
            raise  QueryConditionIsEmptyException(u'Missing "cate_id" key parameters!')

        item = VulnCategoryInfo.objects.get(**sql_where)
        if item:
            if name:
                item.name = name.strip()
            if parent:
                parent = VulnCategoryInfo.objects.filter(id=parent).first()
                item.parent = parent
            if key:
                item.key = key.strip()
            if tag:
                item.tag = tag.strip()

            item.save()
            cache.set('{0}:{1}'.format(VULN_CACHE[3], cate_id), None, 0)
            result = item
    except VulnCategoryInfo.DoesNotExist as ex:
        logger.warning(ex)
    return result


def get_cate_obj_by_id(cate_id):
    """

    :param cate_id:
    :return:
    """
    if cate_id:
        cache_key = '{0}:{1}'.format(VULN_CACHE[3], cate_id)
        cache_obj = cache.get(cache_key)
        if cache_obj:
            return cache_obj
    obj = _get_cate_obj(cate_id=cate_id)
    if obj:
        cache.set(cache_key, obj, VULN_CACHE[0])
    return obj


def get_cate_obj_by_name(name):
    """

    :param name:
    :return:
    """
    return _get_cate_obj(name=name)


def get_origin_obj_by_id(cate_id):
    """

    :param cate_id:
    :return:
    """
    return _get_cate_obj(cate_id=cate_id)


def get_all_list():
    """

    :return:
    """
    cache_obj = cache.get(VULN_CACHE[4])

    if cache_obj:
        return cache_obj
    cate_list = VulnCategoryInfo.objects.all()
    if cate_list:
        cache.set(VULN_CACHE[4], cate_list, None)
    return cate_list


def get_origin_all_list():
    """

    :return:
    """
    cache_obj = cache.get(VULN_CACHE[5])

    if cache_obj:
        return cache_obj
    cate_list = TagInfo.objects.filter(parent__id=1)
    if cate_list:
        cache.set(VULN_CACHE[5], cate_list, None)
    return cate_list
