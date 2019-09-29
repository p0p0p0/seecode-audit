# coding: utf-8
from __future__ import unicode_literals

from django.core.cache import cache

from seecode.libs.core.data import logger
from seecode.apps.project.models.item import RepositoryInfo
from seecode.libs.units import close_old_connections
from seecode.libs.core.exceptions import ParameterIsEmptyException
from seecode.libs.core.exceptions import QueryConditionIsEmptyException
from seecode.libs.core.cache_key import PROJECT_REPO_CACHE


def create_repository_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    name = kwargs.get('name', None)
    merged = kwargs.get('merged', False)
    protected = kwargs.get('protected', False)
    developers_can_push = kwargs.get('developers_can_push', False)
    developers_can_merge = kwargs.get('developers_can_merge', False)
    last_commit_id = kwargs.get('last_commit_id', None)
    last_short_id = kwargs.get('last_short_id', None)
    last_author_email = kwargs.get('last_author_email', None)
    last_author_name = kwargs.get('last_author_name', None)
    last_title = kwargs.get('last_title', None)
    project_obj = kwargs.get('project_obj', None)
    committed_date = kwargs.get('committed_date', None)
    repo_type = kwargs.get('type', 1)

    if not name:
        raise ParameterIsEmptyException(u'Repository name cannot be empty!')

    if last_title and len(last_title) > 255:
        last_title = last_title[:255]

    if last_author_email and len(last_author_email) > 255:
        last_author_email = last_author_email[:255]

    if last_author_name and len(last_author_name) > 255:
        last_author_name = last_author_name[:255]

    if name and len(name) > 128:
        name = name[:128]

    if merged:
        merged = True
    if protected:
        protected = True
    if developers_can_push:
        developers_can_push = True
    if developers_can_merge:
        developers_can_merge = True

    close_old_connections()

    repo = RepositoryInfo(
        name=name,
        merged=merged,
        protected=protected,
        developers_can_push=developers_can_push,
        developers_can_merge=developers_can_merge,
        last_commit_id=last_commit_id,
        last_short_id=last_short_id,
        last_author_email=last_author_email,
        last_author_name=last_author_name,
        last_title=last_title,
        project=project_obj,
        type=repo_type,
    )

    if committed_date:
        repo.committed_date = committed_date

    repo.save()
    return repo


def _get_repository_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    result = None
    repo_id = kwargs.get('repo_id', None)
    name = kwargs.get('name', None)
    project_id = kwargs.get('project_id', None)
    close_old_connections()

    try:
        sql_where = {}

        if repo_id:
            sql_where['id'] = int(repo_id)
        if name:
            sql_where['name'] = name.strip()
        if project_id:
            sql_where['project__id'] = project_id

        if not sql_where:
            raise QueryConditionIsEmptyException(u'Missing "repo_id, name, project_id" key parameters!')

        item = RepositoryInfo.objects.filter(**sql_where).first()
        result = item
    except RepositoryInfo.DoesNotExist as ex:
        logger.warning(ex)
    return result


def update_repository_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    result = None
    repo_id = kwargs.get('repo_id', None)
    name = kwargs.get('name', None)
    merged = kwargs.get('merged', False)
    protected = kwargs.get('protected', False)
    developers_can_push = kwargs.get('developers_can_push', False)
    developers_can_merge = kwargs.get('developers_can_merge', False)
    last_commit_id = kwargs.get('last_commit_id', None)
    last_short_id = kwargs.get('last_short_id', None)
    last_author_email = kwargs.get('last_author_email', None)
    last_author_name = kwargs.get('last_author_name', None)
    last_title = kwargs.get('last_title', None)
    committed_date = kwargs.get('committed_date', None)

    if merged:
        merged = True
    if protected:
        protected = True
    if developers_can_push:
        developers_can_push = True
    if developers_can_merge:
        developers_can_merge = True

    try:
        sql_where = {}

        if repo_id:
            sql_where['id'] = int(repo_id)

        if not sql_where:
            raise QueryConditionIsEmptyException(u'Missing "repo_id" key parameters!')

        item = RepositoryInfo.objects.get(**sql_where)
        if item:
            if name:
                item.name = name.strip()
            if last_commit_id:
                item.last_commit_id = last_commit_id
            if last_short_id:
                item.last_short_id = last_short_id
            if last_author_email:
                item.last_author_email = last_author_email
            if last_author_name:
                item.last_author_name = last_author_name
            if last_author_email:
                item.last_title = last_title
            if committed_date:
                item.committed_date = committed_date
            if merged:
                item.merged = merged
            if protected:
                item.protected = protected
            if developers_can_push:
                item.developers_can_push = developers_can_push
            if developers_can_merge:
                item.developers_can_merge = developers_can_merge

            item.save()
            cache.set('{0}:{1}'.format(PROJECT_REPO_CACHE[1], repo_id), None, 0)

            result = item
    except RepositoryInfo.DoesNotExist as ex:
        logger.warning(ex)
    return result


def get_repository_by_id(repo_id):
    """

    :param repo_id:
    :return:
    """

    cache_key = '{0}:{1}'.format(PROJECT_REPO_CACHE[1], repo_id)
    cache_obj = cache.get(cache_key)
    if cache_obj:
        return cache_obj
    obj = _get_repository_obj(repo_id=repo_id)
    if obj:
        cache.set(cache_key, obj, PROJECT_REPO_CACHE[0])
    return obj


def get_repository_by_name(name, project_id):
    """

    :param name:
    :param project_id:
    :return:
    """
    cache_key = '{0}:{1}_{2}'.format(PROJECT_REPO_CACHE[1], project_id, name)
    cache_obj = cache.get(cache_key)
    if cache_obj:
        return cache_obj
    obj = _get_repository_obj(name=name, project_id=project_id)
    if obj:
        cache.set(cache_key, obj, PROJECT_REPO_CACHE[0])
    return obj


def create_or_update(**kwargs):
    """

    :param kwargs:
    :return:
    """
    name = kwargs.get('name', None)
    project_obj = kwargs.get('project_obj', None)
    repo_obj = get_repository_by_name(name=name, project_id=project_obj.id)
    if repo_obj:
        kwargs['repo_id'] = repo_obj.id
        return update_repository_obj(**kwargs)
    else:
        return create_repository_obj(**kwargs)
