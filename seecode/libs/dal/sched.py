# coding: utf-8
from __future__ import unicode_literals

import timezone_field

from django.core.cache import cache

from seecode.libs.core.data import logger
from seecode.apps.system.models import SchedInfo
from django_celery_beat.models import CrontabSchedule
from django_celery_beat.models import  IntervalSchedule
from seecode.libs.units import close_old_connections
from seecode.libs.core.exceptions import ParameterIsEmptyException
from seecode.libs.core.exceptions import QueryConditionIsEmptyException
from seecode.libs.core.cache_key import SYSTEM_CACHE


def create_sched_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    name = kwargs.get('name', None)
    sched_type = kwargs.get('type', None)
    value = kwargs.get('value', None)


    if not all((name, value, sched_type,)):
        raise ParameterIsEmptyException(u'"name, value, sched_type" parameters cannot be empty !')

    if sched_type:
        sched_type = int(sched_type)

    close_old_connections()

    if sched_type == 1:
        tri = _get_interval(seconds=value)
        if not tri:
            value = int(value)
            tri = IntervalSchedule(
                every=value * 60,
                period='seconds'
            )
            tri.save()

    else:
        tri = _get_crontab(cron_expression=value)
        if not tri:
            minute, hour, day_of_week, day_of_month, month_of_year = value.split(' ')
            tri = CrontabSchedule(
                minute=minute,
                hour=hour,
                day_of_week=day_of_week,
                day_of_month=day_of_month,
                month_of_year=month_of_year,
                timezone='Asia/Shanghai',
            )
            tri.save()

    sched = SchedInfo(
        name=name,
        type=int(sched_type),
    )
    if sched_type == 1:
        sched.interval = tri
    else:
        sched.crontab = tri
    sched.save()
    return sched


def _get_crontab(**kwargs):
    """

    :param kwargs:
    :return:
    """
    result = None
    cron_expression = kwargs.get('cron_expression', None)
    cron_id = kwargs.get('cron_id', None)
    close_old_connections()
    try:
        if cron_expression:
            cron_expression = cron_expression.strip()
            minute, hour, day_of_week, day_of_month, month_of_year = cron_expression.split(' ')
            result = CrontabSchedule.objects.get(
                minute=minute,
                hour=hour,
                day_of_week= day_of_week,
                day_of_month=day_of_month,
                month_of_year=month_of_year)
        if cron_id:
            result = CrontabSchedule.objects.get(id=int(cron_id))
    except CrontabSchedule.DoesNotExist as ex:
        logger.warning(ex)
    return result


def _get_interval(**kwargs):
    """

        :param kwargs:
        :return:
    """
    result = None
    seconds = kwargs.get('seconds', None)
    interval_id = kwargs.get('interval_id', None)
    close_old_connections()
    try:
        if seconds:
            seconds = int(seconds.strip())
            result = IntervalSchedule.objects.get(
                every=seconds * 60,
                period='seconds')
        if interval_id:
            result = IntervalSchedule.objects.get(id=int(interval_id))
    except IntervalSchedule.DoesNotExist as ex:
        logger.warning(ex)
    return result


def _get_sched_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    result = None
    sched_id = kwargs.get('sched_id', None)
    close_old_connections()

    try:

        sql_where = {}

        if sched_id:
            sql_where['id'] = int(sched_id)

        if not sql_where:
            raise QueryConditionIsEmptyException(u'Missing "sched_id" key parameters!')

        item = SchedInfo.objects.get(**sql_where)
        result = item
    except SchedInfo.DoesNotExist as ex:
        logger.warning(ex)
    return result


def update_sched_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    result = None
    issue_id = kwargs.get('issue_id', None)
    code_segment = kwargs.get('code_segment', None)
    is_false_positives = kwargs.get('is_false_positives', None)
    severity = kwargs.get('severity', None)
    status = kwargs.get('status', None)

    try:
        sql_where = {}

        if issue_id:
            sql_where['id'] = int(issue_id)

        if not sql_where:
            raise  QueryConditionIsEmptyException(u'Missing "issue_id" key parameters!')

        item = SchedInfo.objects.get(**sql_where)
        if item:
            if is_false_positives:
                is_false_positives = True
            else:
                is_false_positives = False

            if code_segment:
                item.code_segment = code_segment

            if severity:
                item.severity = severity.strip()
            if status !=None:
                item.status = int(status)

            item.is_false_positives = is_false_positives
            item.save()
            cache.set('{0}:{1}'.format(SYSTEM_CACHE[4], item.id), None, 0)
            result = item
    except SchedInfo.DoesNotExist as ex:
        pass  # FIXME log
    return result


def get_sched_by_id(sched_id):
    """

    :param sched_id:
    :return:
    """
    if sched_id:
        cache_key = '{0}:{1}'.format(SYSTEM_CACHE[4], sched_id)
        cache_obj = cache.get(cache_key)
        if cache_obj:
            return cache_obj
    obj = _get_sched_obj(sched_id=sched_id)
    if obj:
        cache.set(cache_key, obj, SYSTEM_CACHE[0])
    return obj


def get_trigger_by_cron_id(cron_id):
    """

    :param cron_id:
    :return:
    """
    return _get_crontab(cron_id=cron_id)


def get_trigger_by_interval_id(interval_id):
    """

    :param interval_id:
    :return:
    """
    return _get_interval(cron_id=interval_id)

def get_sched_all():
    """

    :return:
    """
    return SchedInfo.objects.all()