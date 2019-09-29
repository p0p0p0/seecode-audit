# coding: utf-8
from __future__ import unicode_literals

from django.core.cache import cache

from seecode.libs.core.data import logger
from seecode.apps.system.models import TagInfo
from seecode.libs.units import close_old_connections
from seecode.libs.core.exceptions import ParameterIsEmptyException
from seecode.libs.core.exceptions import QueryConditionIsEmptyException


def create_tag_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    name = kwargs.get('name', None)
    description = kwargs.get('description', None)
    parent = kwargs.get('parent', None)

    if not all((name, )):
        raise ParameterIsEmptyException(u'"name" parameters cannot be empty !')

    if name and len(name)>64:
        name = name[:64]

    close_old_connections()

    tag = TagInfo(
        name=name,
        description=description,
        parent=parent,
    )
    tag.save()
    return tag


def _get_tag_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    result = None
    tag_id = kwargs.get('tag_id', None)
    parent_id = kwargs.get('parent_id', None)
    name = kwargs.get('name', None)
    close_old_connections()

    try:
        sql_where = {}
        if tag_id:
            sql_where['id'] = int(tag_id)
        if parent_id:
            sql_where['parent__id'] = int(parent_id)
        if name:
            sql_where['name'] = name
        if not sql_where:
            raise QueryConditionIsEmptyException(u'Missing "parent_id, name" key parameters!')

        item = TagInfo.objects.get(**sql_where)
        result = item
    except TagInfo.DoesNotExist as ex:
        logger.warning(ex)
    return result


def update_tag_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    result = None
    tag_id = kwargs.get('tag_id', None)
    name = kwargs.get('name', None)

    try:
        sql_where = {}
        if tag_id:
            sql_where['id'] = int(tag_id)

        if not sql_where:
            raise  QueryConditionIsEmptyException(u'Missing "tag_id" key parameters!')

        item = TagInfo.objects.get(**sql_where)
        if item:
            item.name = name.strip()
            item.save()
            result = item
    except TagInfo.DoesNotExist as ex:
        logger.warning(ex)
    return result


def get_tag_obj_by_id(tag_id):
    """

    :param tag_id:
    :return:
    """
    return _get_tag_obj(tag_id=tag_id)


def get_tag_obj_by_name(name):
    """

    :param name:
    :return:
    """
    return _get_tag_obj(name=name)


def bulk_tag(tags, tag_type):
    """

    :param tags:
    :param tag_type:
    :return:
    """
    result = []
    tags = tags.split(",")
    for tag in tags:
        tag_obj = TagInfo.objects.filter(name__iexact=tag.strip()).first()
        if not tag_obj:
            tag_obj = TagInfo(name=tag.strip(), parent_id=tag_type)
            tag_obj.save()
        result.append(tag_obj)
    return result
