# coding: utf-8
from __future__ import unicode_literals

from django.core.cache import cache

from seecode.libs.core.data import logger
from seecode.apps.project.models.app import DependentInfo
from seecode.libs.units import close_old_connections
from seecode.libs.core.exceptions import ParameterIsEmptyException
from seecode.libs.core.exceptions import QueryConditionIsEmptyException
from seecode.libs.core.cache_key import PROJECT_APP_CACHE


def create_dependent_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    app_obj = kwargs.get('app_obj', None)
    name = kwargs.get('name', None)
    file_name = kwargs.get('file_name', None)
    full_path = kwargs.get('full_path', '')
    group_id = kwargs.get('group_id', None)
    artifact_id = kwargs.get('artifact_id', '')
    version = kwargs.get('version', '')
    new_version = kwargs.get('new_version', '')
    description = kwargs.get('description', '')
    language = kwargs.get('language', '')

    if not all((app_obj, name, file_name)):
        raise ParameterIsEmptyException(u'"app_obj, name, file_name" parameters cannot be empty !')

    close_old_connections()

    dep = DependentInfo(
        app=app_obj,
        name=name,
        file_name=file_name,
        full_path=full_path,
        group_id=group_id,
        artifact_id=artifact_id,
        version=version,
        new_version=new_version,
        description=description,
        language=language,
    )
    dep.save()
    return dep


def _get_dependent_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    result = None
    dep_id = kwargs.get('dep_id', None)
    app_id = kwargs.get('app_id', None)
    name = kwargs.get('name', None)
    group_id = kwargs.get('group_id', None)
    artifact_id = kwargs.get('artifact_id', None)
    close_old_connections()

    try:
        sql_where = {}
        if dep_id:
            sql_where['id'] = int(dep_id)
        if app_id:
            sql_where['app__id'] = int(app_id)
        if name:
            sql_where['name'] = name.strip()
        if group_id:
            sql_where['group_id'] = group_id.strip()
        if artifact_id:
            sql_where['artifact_id'] = artifact_id.strip()

        if not sql_where:
            raise QueryConditionIsEmptyException(u'Missing "dep_id, name" key parameters!')

        item = DependentInfo.objects.get(**sql_where)
        result = item
    except DependentInfo.DoesNotExist as ex:
        logger.warning(ex)
    return result


def update_dependent_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    result = None
    dep_id = kwargs.get('dep_id', None)
    version = kwargs.get('version', '')
    new_version = kwargs.get('new_version', '')
    description = kwargs.get('description', '')
    language = kwargs.get('language', '')

    try:
        sql_where = {}
        if dep_id:
            sql_where['id'] = int(dep_id)
        if not sql_where:
            raise QueryConditionIsEmptyException(u'Missing "dep_id" key parameters!')

        item = DependentInfo.objects.get(**sql_where)
        if item:
            if version:
                item.version = version
            if new_version:
                item.new_version = new_version
            if description:
                item.description = description.strip()
            if language:
                item.language = language.strip()

            item.save()
            cache.set('{0}:{1}'.format(PROJECT_APP_CACHE[2], item.id), None, 0)
            result = item
    except DependentInfo.DoesNotExist as ex:
        logger.warning(ex)
    return result


def update_dependent_version(dep_id, version, new_version=None):
    """

    :param dep_id:
    :param version:
    :param new_version:
    :return:
    """
    return update_dependent_obj(
        dep_id=dep_id,
        version=version,
        new_version=new_version,
    )


def get_dependent_by_id(dep_id):
    """

    :param dep_id:
    :return:
    """

    cache_key = '{0}:{1}'.format(PROJECT_APP_CACHE[2], dep_id)
    cache_obj = cache.get(cache_key)
    if cache_obj:
        return cache_obj
    obj = _get_dependent_obj(dep_id=dep_id)
    if obj:
        cache.set(cache_key, obj, PROJECT_APP_CACHE[0])
    return obj


def get_dependent_by_name(name, app_id):
    """

    :param name:
    :param app_id:
    :return:
    """
    return _get_dependent_obj(name=name, app_id=app_id)


def get_dependent_by_artifact_id(artifact_id, app_id):
    """

    :param artifact_id:
    :param app_id:
    :return:
    """
    return _get_dependent_obj(artifact_id=artifact_id, app_id=app_id)


def create_or_update(**kwargs):
    """

    :param kwargs:
    :return:
    """
    name = kwargs.get('name', None)
    group_id = kwargs.get('group_id', None)
    artifact_id = kwargs.get('artifact_id', None)
    app_obj = kwargs.get('app_obj', None)
    dep_obj = _get_dependent_obj(app_id=app_obj.id, name=name, artifact_id=artifact_id, group_id=group_id)
    if dep_obj:
        kwargs['dep_id'] = dep_obj.id
        return update_dependent_obj(**kwargs)
    else:
        return create_dependent_obj(**kwargs)


def delete_dependent_by_app_id(app_id):
    """

    :param app_id:
    :return:
    """
    if app_id:
        app_list = DependentInfo.objects.filter(app__id=app_id)
        for item in app_list:
            cache_key = '{0}:{1}'.format(PROJECT_APP_CACHE[2], item.id)
            cache.set(cache_key, None, 0)
            item.delete()
