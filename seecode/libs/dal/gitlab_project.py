# coding: utf-8
from __future__ import unicode_literals

from django.core.cache import cache

from seecode.apps.project.models.item import ProjectInfo
from seecode.apps.project.models.item import ProjectPermissionInfo
from seecode.libs.core.cache_key import PROJECT_INFO_CACHE
from seecode.libs.core.data import logger
from seecode.libs.core.exceptions import ParameterIsEmptyException
from seecode.libs.core.exceptions import QueryConditionIsEmptyException
from seecode.libs.units import close_old_connections


def create_project_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    group = kwargs.get('group_obj', None)
    git_id = kwargs.get('git_id', None)
    git_created_at = kwargs.get('git_created_at', None)
    ssh_url_to_repo = kwargs.get('ssh_url_to_repo', None)
    http_url_to_repo = kwargs.get('http_url_to_repo', None)
    web_url = kwargs.get('web_url', '')
    default_branch = kwargs.get('default_branch', '')
    name = kwargs.get('name', None)
    path = kwargs.get('path', None)
    path_with_namespace = kwargs.get('path_with_namespace', '')
    creator_id = kwargs.get('creator_id', None)
    description = kwargs.get('description', '')
    star_count = kwargs.get('star_count', 0)
    forks_count = kwargs.get('forks_count', 0)
    open_issues_count = kwargs.get('open_issues_count', 0)
    visibility_level = kwargs.get('visibility_level', 0)
    project_type = kwargs.get('type', 1)
    is_new = kwargs.get('is_new', True)
    git_last_activity_at = kwargs.get('git_last_activity_at', None)
    issues_enabled = kwargs.get('issues_enabled', True)
    user = kwargs.get('user', None)
    file_hash = kwargs.get('file_hash', None)
    file_size = kwargs.get('file_size', 0)
    file_origin_name = kwargs.get('file_origin_name', None)

    if not name:
        raise ParameterIsEmptyException(u'Project name cannot be empty!')

    if git_created_at:
        git_created_at = git_created_at

    if creator_id is not None:
        creator_id = int(creator_id)

    if star_count is not None:
        star_count = int(star_count)

    if forks_count is not None:
        forks_count = int(forks_count)

    if open_issues_count is not None:
        open_issues_count = int(open_issues_count)

    if visibility_level is not None:
        visibility_level = int(visibility_level)

    if project_type is not None:
        project_type = int(project_type)

    close_old_connections()

    project = ProjectInfo(
        group=group,
        git_id=git_id,
        git_created_at=git_created_at,
        git_last_activity_at=git_last_activity_at,
        issues_enabled=issues_enabled,
        ssh_url_to_repo=ssh_url_to_repo,
        http_url_to_repo=http_url_to_repo,
        web_url=web_url,
        default_branch=default_branch,
        name=name,
        path=path,
        path_with_namespace=path_with_namespace,
        creator_id=creator_id,
        description=description,
        star_count=star_count,
        forks_count=forks_count,
        open_issues_count=open_issues_count,
        visibility_level=visibility_level,
        type=project_type,
        user=user,
        is_new=is_new,
        file_hash=file_hash,
        file_size=file_size,
        file_origin_name=file_origin_name
    )
    project.save()
    return project


def create_pro_member_perm_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    project_obj = kwargs.get('project_obj', None)
    member_obj = kwargs.get('member_obj', None)
    access_level = kwargs.get('access_level', None)
    expires_at = kwargs.get('git_created_at', None)

    close_old_connections()

    perm = ProjectPermissionInfo(
        project=project_obj,
        member=member_obj,
        access_level=access_level,
        expires_at=expires_at
    )
    perm.save()
    return perm


def _get_project_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    result = None
    git_id = kwargs.get('git_id', None)
    project_id = kwargs.get('project_id', None)
    name = kwargs.get('name', None)
    ssh_url = kwargs.get('ssh_url', None)
    close_old_connections()

    try:
        sql_where = {}

        if git_id:
            sql_where['git_id'] = int(git_id)
        if project_id:
            sql_where['id'] = int(project_id)
        if name:
            sql_where['name'] = name.strip()
        if ssh_url:
            sql_where['ssh_url_to_repo__iexact'] = ssh_url.strip()

        if not sql_where:
            raise QueryConditionIsEmptyException(u'Missing "project_id, git_id, name" key parameters!')

        item = ProjectInfo.objects.get(**sql_where)
        result = item
    except ProjectInfo.DoesNotExist as ex:
        logger.warning(ex)
    return result


def _get_pro_member_perm(**kwargs):
    """

    :param kwargs:
    :return:
    """
    result = None
    member_id = kwargs.get('member_id', None)
    project_id = kwargs.get('project_id', None)
    close_old_connections()

    try:
        sql_where = {}

        if member_id:
            sql_where['member__id'] = int(member_id)
        if project_id:
            sql_where['project__id'] = int(project_id)
        if not sql_where:
            raise QueryConditionIsEmptyException(u'Missing "member_id, project_id" key parameters!')

        result = ProjectPermissionInfo.objects.filter(**sql_where).first()

    except ProjectPermissionInfo.DoesNotExist as ex:
        logger.warning(ex)
    return result


def update_project_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    result = None
    project_id = kwargs.get('project_id', None)
    git_id = kwargs.get('git_id', None)
    ssh_url_to_repo = kwargs.get('ssh_url_to_repo', None)
    http_url_to_repo = kwargs.get('http_url_to_repo', None)
    git_last_activity_at = kwargs.get('git_last_activity_at', None)
    web_url = kwargs.get('web_url', None)
    default_branch = kwargs.get('default_branch', None)
    name = kwargs.get('name', None)
    path = kwargs.get('path', None)
    path_with_namespace = kwargs.get('path_with_namespace', None)
    creator_id = kwargs.get('creator_id', None)
    description = kwargs.get('description', None)
    star_count = kwargs.get('star_count', None)
    forks_count = kwargs.get('forks_count', None)
    open_issues_count = kwargs.get('open_issues_count', None)
    visibility_level = kwargs.get('visibility_level', None)
    is_new = kwargs.get('is_new', False)
    department = kwargs.get('department', None)

    try:
        sql_where = {}
        if project_id:
            sql_where['id'] = int(project_id)
        if git_id:
            sql_where['git_id'] = int(git_id)
        if not sql_where:
            raise QueryConditionIsEmptyException(u'Missing "project_id, git_id" key parameters!')

        item = ProjectInfo.objects.get(**sql_where)
        if item:
            if name:
                item.name = name.strip()
            if path:
                item.path = path.strip()
            if description:
                item.description = description.strip()
            if web_url:
                item.web_url = web_url.strip()
            if ssh_url_to_repo:
                item.ssh_url_to_repo = ssh_url_to_repo.strip()
            if http_url_to_repo:
                item.http_url_to_repo = http_url_to_repo.strip()
            if default_branch:
                item.default_branch = default_branch.strip()
            if visibility_level:
                item.visibility_level = int(visibility_level)
            if path_with_namespace:
                item.path_with_namespace = path_with_namespace.strip()
            if creator_id:
                item.creator_id = int(creator_id)
            if star_count:
                item.star_count = int(star_count)
            if forks_count:
                item.forks_count = int(forks_count)
            if open_issues_count:
                item.open_issues_count = int(open_issues_count)
            if department:
                item.department = department
            if is_new:
                item.is_new = True
            else:
                item.is_new = False
            if git_last_activity_at:
                item.git_last_activity_at = git_last_activity_at

            item.save()
            cache.set('{0}:{1}'.format(PROJECT_INFO_CACHE[1], item.id), None, 0)
            cache.set('{0}:{1}'.format(PROJECT_INFO_CACHE[1], item.ssh_url_to_repo), None, 0)
            cache.set('{0}:{1}'.format(PROJECT_INFO_CACHE[2], item.git_id), None, 0)
            result = item
    except ProjectInfo.DoesNotExist as ex:
        logger.warning(ex)
    return result


def get_project_by_id(project_id):
    """

    :param project_id:
    :return:
    """
    cache_key = '{0}:{1}'.format(PROJECT_INFO_CACHE[1], project_id)
    cache_obj = cache.get(cache_key)
    if cache_obj:
        return cache_obj
    obj = _get_project_obj(project_id=project_id)
    if obj:
        cache.set(cache_key, obj, PROJECT_INFO_CACHE[0])
    return obj


def get_project_by_ssh_url(ssh_url):
    """
    :param ssh_url:
    :return:
    """
    cache_key = '{0}:{1}'.format(PROJECT_INFO_CACHE[1], ssh_url)
    cache_obj = cache.get(cache_key)
    if cache_obj:
        return cache_obj
    obj = _get_project_obj(ssh_url=ssh_url)
    if obj:
        cache.set(cache_key, obj, PROJECT_INFO_CACHE[0])
    return obj


def get_project_by_gitid(git_id):
    """

    :param git_id:
    :return:
    """
    cache_key = '{0}:{1}'.format(PROJECT_INFO_CACHE[2], git_id)
    cache_obj = cache.get(cache_key)
    if cache_obj:
        return cache_obj
    obj = _get_project_obj(git_id=git_id)
    if obj:
        cache.set(cache_key, obj, PROJECT_INFO_CACHE[0])
    return obj


def get_project_by_name(name):
    """

    :param name:
    :return:
    """
    return _get_project_obj(name=name)


def create_or_update(**kwargs):
    """

    :param kwargs:
    :return:
    """
    git_id = kwargs.get('git_id', None)
    project_obj = get_project_by_gitid(git_id=git_id)
    if project_obj:
        return update_project_obj(**kwargs)
    else:
        return create_project_obj(**kwargs)


def get_project_list_by_group_id(group_id):
    """

    :param group_id:
    :return:
    """
    return ProjectInfo.objects.filter(group__id=int(group_id))


def get_project_top50():
    """

    :return:
    """
    cache_obj = cache.get(PROJECT_INFO_CACHE[3])
    if cache_obj:
        return cache_obj
    obj = ProjectInfo.objects.filter()[:50]
    if obj:
        cache.set(PROJECT_INFO_CACHE[3], obj, 60 * 15)
    return obj


def get_pro_member_perm(member_id, project_id):
    """

    :param member_id:
    :param project_id:
    :return:
    """
    cache_key = '{0}:{1}_{2}'.format(PROJECT_INFO_CACHE[2], project_id, member_id)
    cache_obj = cache.get(cache_key)
    if cache_obj:
        return cache_obj
    obj = _get_pro_member_perm(member_id=member_id, project_id=project_id)
    if obj:
        cache.set(cache_key, obj, PROJECT_INFO_CACHE[0])
    return obj


def get_pro_all_member_perm(project_id):
    """
    :param project_id:
    :return:
    """
    cache_key = '{0}:{1}:members'.format(PROJECT_INFO_CACHE[2], project_id)
    cache_obj = cache.get(cache_key)
    if cache_obj:
        return cache_obj
    project_members = ProjectPermissionInfo.objects.filter(project__id=project_id, member__state='active')
    if project_members:
        cache.set(cache_key, project_members, PROJECT_INFO_CACHE[0])
    return project_members


def clear_pro_all_member_perm(project_id):
    cache_key = '{0}:{1}:members'.format(PROJECT_INFO_CACHE[2], project_id)
    cache.set(cache_key, None, 0)
