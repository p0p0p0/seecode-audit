# coding: utf-8
from __future__ import unicode_literals

from django.core.cache import cache

from seecode.libs.core.data import logger
from seecode.apps.project.models.group import GroupInfo
from seecode.apps.project.models.group import GroupPermissionInfo
from seecode.libs.units import close_old_connections
from seecode.libs.core.exceptions import ParameterIsEmptyException
from seecode.libs.core.exceptions import QueryConditionIsEmptyException
from seecode.libs.core.cache_key import PROJECT_GROUP_CACHE


def create_group_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    git_id = kwargs.get('git_id', None)
    name = kwargs.get('name', '')
    path = kwargs.get('path', '')
    description = kwargs.get('description', None)
    web_url = kwargs.get('web_url', '')
    full_name = kwargs.get('full_name', '')
    full_path = kwargs.get('full_path', None)
    parent_id = kwargs.get('parent_id', None)
    visibility_level = kwargs.get('visibility_level', 0)
    group_type = kwargs.get('type', 1)
    user = kwargs.get('user', None)

    if not name:
        raise ParameterIsEmptyException(u'Group name cannot be empty!')

    if name and len(name) > 128:
        name = name[:128]
    if group_type:
        group_type = int(group_type)

    close_old_connections()

    group = GroupInfo(
        git_id=git_id,
        name=name,
        description=description,
        web_url=web_url,
        full_name=full_name,
        path=path,
        full_path=full_path,
        parent_id=parent_id,
        visibility_level=visibility_level,
        type=group_type,
        user=user,
    )
    group.save()
    return group


def create_group_member_perm_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    group_obj = kwargs.get('group_obj', None)
    member_obj = kwargs.get('member_obj', None)
    access_level = kwargs.get('access_level', None)
    expires_at = kwargs.get('git_created_at', None)

    close_old_connections()

    perm = GroupPermissionInfo(
        group=group_obj,
        member=member_obj,
        access_level=access_level,
        expires_at=expires_at
    )
    perm.save()
    return perm


def _get_group_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    git_id = kwargs.get('git_id', None)
    group_id = kwargs.get('group_id', None)
    name = kwargs.get('name', None)
    close_old_connections()

    try:
        sql_where = {}
        if git_id:
            sql_where['git_id'] = int(git_id)
        if group_id:
            sql_where['id'] = int(group_id)
        if name:
            sql_where['name'] = name.strip()

        if not sql_where:
            raise QueryConditionIsEmptyException(u'Missing "group_id, git_id, name" key parameters!')

        item = GroupInfo.objects.filter(**sql_where).first()
        return item
    except GroupInfo.DoesNotExist as ex:
        logger.warning(ex)
        return None


def _get_group_member_perm(**kwargs):
    """

    :param kwargs:
    :return:
    """
    result = None
    member_id = kwargs.get('member_id', None)
    group_id = kwargs.get('group_id', None)
    close_old_connections()

    try:
        sql_where = {}
        if member_id:
            sql_where['member__id'] = int(member_id)
        if group_id:
            sql_where['group__id'] = int(group_id)
        if not sql_where:
            raise QueryConditionIsEmptyException(u'Missing "member_id, group_id" key parameters!')

        result = GroupPermissionInfo.objects.get(**sql_where)

    except GroupPermissionInfo.DoesNotExist as ex:
        logger.warning(ex)
    return result


def update_group_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    group_id = kwargs.get('group_id', None)
    git_id = kwargs.get('git_id', None)
    name = kwargs.get('name', None)
    path = kwargs.get('path', '')
    description = kwargs.get('description', None)
    web_url = kwargs.get('web_url', '')
    full_name = kwargs.get('full_name', '')
    full_path = kwargs.get('full_path', None)
    parent_id = kwargs.get('parent_id', None)
    visibility_level = kwargs.get('visibility_level', None)

    try:
        sql_where = {}
        if group_id:
            sql_where['id'] = int(group_id)
        if git_id:
            sql_where['git_id'] = int(git_id)

        if not sql_where:
            raise QueryConditionIsEmptyException(u'Missing "group_id, git_id" key parameters!')

        item = GroupInfo.objects.filter(**sql_where).first()
        if item:
            if name:
                item.name = name.strip()
            if path:
                item.path = path.strip()
            if description:
                item.description = description.strip()
            if web_url:
                item.web_url = web_url.strip()
            if full_name:
                item.full_name = full_name.strip()
            if full_path:
                item.full_path = full_path.strip()
            if parent_id:
                item.parent_id = int(parent_id)
            if visibility_level !=None:
                item.visibility_level = int(visibility_level)

            item.save()
            cache.set('{0}:{1}'.format(PROJECT_GROUP_CACHE[1], item.id), None, 0)
            cache.set('{0}:{1}'.format(PROJECT_GROUP_CACHE[2], item.git_id), None, 0)
        return item
    except GroupInfo.DoesNotExist as ex:
        return None


def delete_group_obj(group_id):
    """

    :param group_id:
    :return:
    """
    try:
        GroupInfo.objects.get(id=int(group_id)).delete()
        return True
    except Exception as ex:
        logger.warning(ex)
        return False


def create_or_update(**kwargs):
    """

    :param kwargs:
    :return:
    """
    git_id = kwargs.get('git_id', None)
    group_obj = get_group_by_gitid(git_id=git_id)
    if group_obj:
        return update_group_obj(**kwargs)
    else:
        return create_group_obj(**kwargs)


def get_or_create(**kwargs):
    """

    :param kwargs:
    :return:
    """
    git_id = kwargs.get('git_id', None)
    group_obj = get_group_by_gitid(git_id=git_id)

    if not group_obj:
        group_obj = create_group_obj(**kwargs)

    return group_obj


def get_group_by_id(group_id):
    """

    :param group_id:
    :return:
    """

    cache_key = '{0}:{1}'.format(PROJECT_GROUP_CACHE[1], group_id)
    cache_obj = cache.get(cache_key)
    if cache_obj:
        return cache_obj
    obj = _get_group_obj(group_id=group_id)
    if obj:
        cache.set(cache_key, obj, PROJECT_GROUP_CACHE[0])
    return obj


def get_group_by_gitid(git_id):
    """

    :param git_id:
    :return:
    """

    cache_key = '{0}:{1}'.format(PROJECT_GROUP_CACHE[2], git_id)
    cache_obj = cache.get(cache_key)
    if cache_obj:
        return cache_obj
    obj = _get_group_obj(git_id=git_id)
    if obj:
        cache.set(cache_key, obj, PROJECT_GROUP_CACHE[0])
    return obj


def get_group_by_name(name):
    """

    :param name:
    :return:
    """
    return _get_group_obj(name=name)


def get_group_top20():
    """

    :return:
    """
    cache_obj = cache.get(PROJECT_GROUP_CACHE[3])
    if cache_obj:
        return cache_obj
    obj = GroupInfo.objects.filter().order_by('-created_at')[:20]
    if obj:
        cache.set(PROJECT_GROUP_CACHE[3], obj, 60*15)
    return obj


def get_group_member_perm(member_id, group_id):
    """

    :param member_id:
    :param group_id:
    :return:
    """
    cache_key = '{0}:{1}_{2}'.format(PROJECT_GROUP_CACHE[2], group_id, member_id)
    cache_obj = cache.get(cache_key)
    if cache_obj:
        return cache_obj
    obj = _get_group_member_perm(member_id=member_id, group_id=group_id)
    if obj:
        cache.set(cache_key, obj, PROJECT_GROUP_CACHE[0])
    return obj


def get_group_all_member_perm(group_id):
    """
    :param group_id:
    :return:
    """
    cache_key = '{0}:{1}:members'.format(PROJECT_GROUP_CACHE[2], group_id)
    cache_obj = cache.get(cache_key)
    if cache_obj:
        return cache_obj
    group_members = GroupPermissionInfo.objects.filter(group__id=group_id, member__state='active')
    if group_members:
        cache.set(cache_key, group_members, PROJECT_GROUP_CACHE[0])
    return group_members


def clear_group_all_member_perm(group_id):
    cache_key = '{0}:{1}:members'.format(PROJECT_GROUP_CACHE[2], group_id)
    cache.set(cache_key, None, 0)
