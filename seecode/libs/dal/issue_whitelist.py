# coding: utf-8
from __future__ import unicode_literals

from django.core.cache import cache

from seecode.libs.core.data import logger
from seecode.apps.scan.models import IssueWhiteListInfo
from seecode.libs.units import close_old_connections
from seecode.libs.core.exceptions import ParameterIsEmptyException
from seecode.libs.core.exceptions import QueryConditionIsEmptyException
from seecode.libs.core.cache_key import ISSUE_CACHE


def create_whitelist_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    issue_obj = kwargs.get('issue_obj', None)
    operator = kwargs.get('operator', None)
    app_obj = kwargs.get('app_obj', None)
    comment = kwargs.get('comment', None)
    is_active = kwargs.get('is_active', True)

    if not all((issue_obj, operator, app_obj)):
        raise ParameterIsEmptyException(u'"issue_obj, operator, app_obj" parameters cannot be empty !')

    if comment:
        comment = comment[:500]

    close_old_connections()

    whitelist = IssueWhiteListInfo(
        issue=issue_obj,
        operator=operator,
        app=app_obj,
        comment=comment,
        is_active=is_active,
    )
    whitelist.save()
    return whitelist


def _get_whitelist_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    result = None
    white_id = kwargs.get('white_id', None)
    issue_id = kwargs.get('issue_id', None)
    close_old_connections()

    try:
        sql_where = {}
        if white_id:
            sql_where['id'] = int(white_id)
        if issue_id:
            sql_where['issue__id'] = int(issue_id)

        if not sql_where:
            raise QueryConditionIsEmptyException(u'Missing "white_id, issue_id" key parameters!')

        item = IssueWhiteListInfo.objects.get(**sql_where)
        result = item
    except IssueWhiteListInfo.DoesNotExist as ex:
        logger.warning(ex)
    return result


def update_whitelist_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    result = None
    white_id = kwargs.get('white_id', None)
    is_active = kwargs.get('is_active', None)

    try:
        sql_where = {}
        if white_id:
            sql_where['id'] = int(white_id)

        if not sql_where:
            raise  QueryConditionIsEmptyException(u'Missing "white_id" key parameters!')

        item = IssueWhiteListInfo.objects.get(**sql_where)
        if item:

            if is_active:
                item.is_active = True
            else:
                item.is_active = False

            item.save()
            cache.set('{0}:{1}'.format(ISSUE_CACHE[1], item.id), None, 0)
            result = item
    except IssueWhiteListInfo.DoesNotExist as ex:
        logger.warning(ex)
    return result


def get_whitelist_by_id(white_id):
    """

    :param white_id:
    :return:
    """
    if white_id:
        cache_key = '{0}:{1}'.format(ISSUE_CACHE[1], white_id)
        cache_obj = cache.get(cache_key)
        if cache_obj:
            return cache_obj
    obj = _get_whitelist_obj(white_id=white_id)
    if obj:
        cache.set(cache_key, obj, ISSUE_CACHE[0])
    return obj


def get_whitelist_by_issue_id(issue_id):
    """

    :param issue_id:
    :return:
    """
    return _get_whitelist_obj(issue_id=issue_id)
