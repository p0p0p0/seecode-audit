# coding: utf-8
from __future__ import unicode_literals

from django.core.cache import cache

from seecode.libs.core.data import logger
from seecode.apps.project.models.app import FileStatisticsInfo
from seecode.libs.units import close_old_connections
from seecode.libs.core.exceptions import ParameterIsEmptyException
from seecode.libs.core.exceptions import QueryConditionIsEmptyException
from seecode.libs.core.cache_key import PROJECT_APP_CACHE


def create_statistics_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    app = kwargs.get('app_obj', None)
    language = kwargs.get('language', None)
    files = kwargs.get('files', None)
    blank = kwargs.get('blank', None)
    comment = kwargs.get('comment', None)
    code = kwargs.get('code', None)

    if not all((app, language)):
        raise ParameterIsEmptyException(u'Language name cannot be empty!')

    close_old_connections()

    if files:
        files = int(files)
    if blank:
        blank = int(blank)
    if comment:
        comment = int(comment)
    if code:
        code = int(code)

    stat = FileStatisticsInfo(
        app=app,
        language=language.strip(),
        files=files,
        blank=blank,
        comment=comment,
        code=code,
    )
    stat.save()
    return stat


def _get_statistics_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    result = None
    stat_id = kwargs.get('stat_id', None)
    language = kwargs.get('language', None)
    app_id = kwargs.get('app_id', None)
    close_old_connections()

    try:
        sql_where = {}

        if stat_id:
            sql_where['id'] = int(stat_id)
        if language:
            sql_where['language__iexact'] = language.strip()
        if app_id:
            sql_where['app__id'] = int(app_id)

        if not sql_where:
            raise QueryConditionIsEmptyException(u'Missing "stat_id, language, app_id" key parameters!')

        item = FileStatisticsInfo.objects.get(**sql_where)
        result = item
    except FileStatisticsInfo.DoesNotExist as ex:
        logger.warning(ex)
    return result


def update_statistics_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    result = None
    stat_id = kwargs.get('stat_id', None)
    files = kwargs.get('files', None)
    blank = kwargs.get('blank', None)
    comment = kwargs.get('comment', None)
    code = kwargs.get('code', None)

    if files:
        files = int(files)
    if blank:
        blank = int(blank)
    if comment:
        comment = int(comment)
    if code:
        code = int(code)

    try:
        sql_where = {}
        if stat_id:
            sql_where['id'] = int(stat_id)
        if not sql_where:
            raise QueryConditionIsEmptyException(u'Missing "stat_id" key parameters!')

        item = FileStatisticsInfo.objects.get(**sql_where)
        if item:
            if files:
                item.files = files
            if blank:
                item.blank = blank
            if comment:
                item.comment = comment
            if code:
                item.code = code

            item.save()
            cache.set('{0}:{1}'.format(PROJECT_APP_CACHE[3], item.id), None, 0)
            result = item
    except FileStatisticsInfo.DoesNotExist as ex:
        logger.warning(ex)
    return result


def get_statistics_by_id(stat_id):
    """

    :param stat_id:
    :return:
    """

    cache_key = '{0}:{1}'.format(PROJECT_APP_CACHE[3], stat_id)
    cache_obj = cache.get(cache_key)
    if cache_obj:
        return cache_obj

    obj = _get_statistics_obj(stat_id=stat_id)
    if obj:
        cache.set(cache_key, obj, PROJECT_APP_CACHE[0])
    return obj


def get_statistics_by_language(language, app_id):
    """

    :param language:
    :param app_id:
    :return:
    """
    if not all((language, app_id, )):
        raise ParameterIsEmptyException(u'"language, app_id" parameters cannot be empty !')
    return _get_statistics_obj(language=language, app_id=app_id)


def create_or_update(**kwargs):
    """

    :param kwargs:
    :return:
    """
    language = kwargs.get('language', None)
    app_obj = kwargs.get('app_obj', None)
    stat_obj = get_statistics_by_language(language=language, app_id=app_obj.id)
    if stat_obj:
        kwargs['stat_id'] = stat_obj.id
        return update_statistics_obj(**kwargs)
    else:
        return create_statistics_obj(**kwargs)
