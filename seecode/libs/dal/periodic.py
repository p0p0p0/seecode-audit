# coding: utf-8
from __future__ import unicode_literals

from django.core.cache import cache
from django_celery_beat.models import PeriodicTask, PeriodicTasks

from seecode.libs.core.data import logger
from seecode.libs.core.exceptions import ParameterIsEmptyException
from seecode.libs.core.exceptions import QueryConditionIsEmptyException
from seecode.libs.units import close_old_connections
from seecode.libs.core.cache_key import SYSTEM_CACHE


def create_periodic_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    name = kwargs.get('name', None)
    task = kwargs.get('task', 'seecode.services.scan.sched_start')
    interval = kwargs.get('interval', None)
    crontab = kwargs.get('crontab', None)
    args = kwargs.get('args', '')
    kkwargs = kwargs.get('kkwargs', '')
    queue = kwargs.get('queue', 'sched')
    exchange = kwargs.get('exchange', None)
    priority = kwargs.get('priority', 1)

    if not all((name, task, queue,)):
        raise ParameterIsEmptyException(u'"name, task, queue" parameters cannot be empty !')

    obj = PeriodicTask(
        name=name,
        task=task,
        interval=interval,
        crontab=crontab,
        args=args,
        kwargs=kkwargs,
        queue=queue,
        exchange=exchange,
        priority=priority,
    )
    obj.save()
    PeriodicTasks.changed(obj)
    return obj


def _get_periodic_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    result = None
    periodic_id = kwargs.get('periodic_id', None)
    task = kwargs.get('task', None)
    name = kwargs.get('name', None)
    close_old_connections()

    try:

        sql_where = {}

        if periodic_id:
            sql_where['id'] = int(periodic_id)
        if task:
            sql_where['task'] = task.strip()
        if name:
            sql_where['name'] = name.strip()

        if not sql_where:
            raise QueryConditionIsEmptyException(u'Missing "periodic_id, task, name" key parameters!')

        item = PeriodicTask.objects.get(**sql_where)
        result = item
    except PeriodicTask.DoesNotExist as ex:
        logger.warning(ex)
    return result


def get_periodic_by_id(periodic_id):
    """

    :param periodic_id:
    :return:
    """
    if periodic_id:
        cache_key = '{0}:{1}'.format(SYSTEM_CACHE[2], periodic_id)
        cache_obj = cache.get(cache_key)
        if cache_obj:
            return cache_obj
    obj = _get_periodic_obj(periodic_id=periodic_id)
    if obj:
        cache.set(cache_key, obj, SYSTEM_CACHE[0])
    return obj


def get_periodic_by_name(name):
    """

    :param name:
    :return:
    """
    return _get_periodic_obj(name=name)


def get_periodic_by_task(task):
    """

    :param task:
    :return:
    """
    return _get_periodic_obj(task=task)


def get_periodic_all():
    """

    :return:
    """
    return PeriodicTask.objects.all()
