# coding: utf-8
from __future__ import unicode_literals

from django.core.cache import cache

from seecode.libs.core.enum import behavior_type
from seecode.libs.core.data import logger
from seecode.apps.scan.models import IssueFlowInfo
from seecode.libs.units import close_old_connections
from seecode.libs.core.exceptions import ParameterIsEmptyException
from seecode.libs.core.exceptions import QueryConditionIsEmptyException


def create_flow_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    issue_obj = kwargs.get('issue_obj', None)
    user = kwargs.get('user', None)
    comment = kwargs.get('comment', None)

    if not all((issue_obj, comment)):
        raise ParameterIsEmptyException(u'"issue_obj, comment" parameters cannot be empty !')

    close_old_connections()

    issue = IssueFlowInfo(
        issue=issue_obj,
        user=user,
        behavior=behavior_type.HUMAN if user else behavior_type.SYS,
        status=issue_obj.status,
        comment=comment,
    )
    issue.save()

    return issue


def _get_flow_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    result = None
    flow_id = kwargs.get('flow_id', None)
    close_old_connections()

    try:
        sql_where = {}

        if flow_id:
            sql_where['id'] = int(flow_id)

        if not sql_where:
            raise QueryConditionIsEmptyException(u'Missing "flow_id" key parameters!')

        item = IssueFlowInfo.objects.get(**sql_where)
        result = item
    except IssueFlowInfo.DoesNotExist as ex:
        logger.warning(ex)
    return result


def get_flow_obj_by_id(flow_id):
    """

    :param flow_id:
    :return:
    """
    return _get_flow_obj(flow_id=flow_id)
