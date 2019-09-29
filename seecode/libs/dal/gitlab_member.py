# coding: utf-8
from __future__ import unicode_literals

from django.core.cache import cache

from seecode.libs.core.data import logger
from seecode.apps.project.models.member import MemberInfo
from seecode.libs.units import close_old_connections
from seecode.libs.core.exceptions import ParameterIsEmptyException
from seecode.libs.core.exceptions import QueryConditionIsEmptyException
from seecode.libs.core.cache_key import PROJECT_MEMBER_CACHE


def create_member_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    git_id = kwargs.get('git_id', None)
    name = kwargs.get('name', None)
    username = kwargs.get('username', None)
    state = kwargs.get('state', None)
    web_url = kwargs.get('web_url', None)
    email = kwargs.get('email', None)
    gitlab_created_at = kwargs.get('gitlab_created_at', None)

    if not name:
        raise ParameterIsEmptyException(u'Member name cannot be empty!')
    if name and len(name) > 64:
        name = name[:64]
    if git_id:
        git_id = int(git_id)
    close_old_connections()

    member = MemberInfo(
        git_id=git_id,
        name=name,
        username=username,
        state=state,
        web_url=web_url,
        email=email,
        gitlab_created_at=gitlab_created_at,
    )
    member.save()
    return member


def _get_member_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    result = None
    git_id = kwargs.get('git_id', None)
    member_id = kwargs.get('member_id', None)
    username = kwargs.get('username', None)
    close_old_connections()

    try:
        sql_where = {}
        if git_id:
            sql_where['git_id'] = int(git_id)
        if member_id:
            sql_where['id'] = int(member_id)
        if username:
            sql_where['username'] = username.strip()
        if not sql_where:
            raise QueryConditionIsEmptyException(u'Missing "member_id, git_id, username" key parameters!')

        item = MemberInfo.objects.filter(**sql_where).first()
        result = item
    except MemberInfo.DoesNotExist as ex:
        logger.warning(ex)
    return result


def get_member_by_id(member_id):
    """

    :param member_id:
    :return:
    """

    cache_key = '{0}:{1}'.format(PROJECT_MEMBER_CACHE[1], member_id)
    cache_obj = cache.get(cache_key)
    if cache_obj:
        return cache_obj
    obj = _get_member_obj(member_id=member_id)
    if obj:
        cache.set(cache_key, obj, PROJECT_MEMBER_CACHE[0])
    return obj


def get_member_by_gitid(git_id):
    """

    :param git_id:
    :return:
    """
    cache_key = '{0}:{1}'.format(PROJECT_MEMBER_CACHE[2], git_id)
    cache_obj = cache.get(cache_key)
    if cache_obj:
        return cache_obj
    obj = _get_member_obj(git_id=git_id)
    if obj:
        cache.set(cache_key, obj, PROJECT_MEMBER_CACHE[0])
    return obj


def get_member_by_username(username):
    """

    :param username:
    :return:
    """
    return _get_member_obj(username=username)


def update_member_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    git_id = kwargs.get('git_id', None)
    member_id = kwargs.get('member_id', None)
    name = kwargs.get('name', None)
    username = kwargs.get('username', None)
    state = kwargs.get('state', None)
    web_url = kwargs.get('web_url', None)
    email = kwargs.get('email', None)
    gitlab_created_at = kwargs.get('gitlab_created_at', None)

    if not name:
        raise ParameterIsEmptyException(u'Member name cannot be empty!')
    if name and len(name) > 64:
        name = name[:64]
    sql_where = {}
    if git_id:
        sql_where['git_id'] = int(git_id)
    if member_id:
        sql_where['id'] = int(member_id)
    if not sql_where:
        raise QueryConditionIsEmptyException(u'Missing "member_id, git_id" key parameters!')
    close_old_connections()
    member = MemberInfo.objects.filter(**sql_where).first()
    if member:
        if name:
            member.name = name
        if username:
            member.username = username
        if state:
            member.state = state
        if web_url:
            member.web_url = web_url
        if email:
            member.email = email
        if gitlab_created_at:
            member.gitlab_created_at = gitlab_created_at

        member.save()
        cache.set('{0}:{1}'.format(PROJECT_MEMBER_CACHE[1], member_id), None, 0)
        cache.set('{0}:{1}'.format(PROJECT_MEMBER_CACHE[2], member.git_id), None, 0)
        return member
    else:
        return None


def create_or_update(**kwargs):
    """

    :param kwargs:
    :return:
    """
    git_id = kwargs.get('git_id', None)
    member_obj = get_member_by_gitid(git_id=git_id)
    if member_obj:
        return update_member_obj(**kwargs)
    else:
        return create_member_obj(**kwargs)
