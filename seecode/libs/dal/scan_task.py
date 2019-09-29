# coding: utf-8
from __future__ import unicode_literals

import datetime

from django.core.cache import cache

from seecode.apps.scan.models import TaskInfo
from seecode.libs.core.log import logger
from seecode.libs.dal.application import get_app_by_id
from seecode.libs.dal.application import create_app_obj
from seecode.libs.dal.application import get_app_by_branch
from seecode.libs.dal.gitlab_project import get_project_by_id
from seecode.libs.dal.gitlab_repository import get_repository_by_name
from seecode.libs.dal.scan_group import get_t_group_by_id
from seecode.libs.dal.application import update_app_statistics
from seecode.libs.dal.application import update_app_obj
from seecode.libs.core.exceptions import ParameterIsEmptyException
from seecode.libs.core.exceptions import QueryConditionIsEmptyException
from seecode.libs.core.exceptions import NotFoundBranchException
from seecode.libs.units import close_old_connections
from seecode.libs.core.cache_key import SCAN_CACHE


def create_task_obj(**kwargs):
    """
    :param kwargs:
    :return:
    """
    app_obj = kwargs.get('app_obj', None)
    group_obj = kwargs.get('group_obj', None)
    executor_ip = kwargs.get('executor_ip', '')
    status = kwargs.get('status', 2)
    is_force_scan = kwargs.get('is_force_scan', False)
    log_file = kwargs.get('log_file', '')
    scan_way = kwargs.get('scan_way', 1)
    error_title = kwargs.get('title', '等待扫描任务被调度')
    error_reason = kwargs.get('reason', '')
    version = kwargs.get('version', '')

    if not all((app_obj, group_obj,)):
        raise ParameterIsEmptyException(u'"app_obj, group_obj" parameters cannot be empty !')

    close_old_connections()

    task = TaskInfo(
        app=app_obj,
        group=group_obj,
        executor_ip=executor_ip,
        template_name=group_obj.profile.name,
        log_file=log_file,
        status=int(status),
        scan_way=int(scan_way),
        is_force_scan=is_force_scan,
        error_title=error_title,
        error_reason=error_reason,
        version=version,
    )
    task.save()

    return task


def create_task_by_app_id(**kwargs):
    """

    :param kwargs:
    :return:
    """
    app_id = kwargs.get('app_id', None)
    group_id = kwargs.get('group_id', None)
    is_force_scan = kwargs.get('is_force_scan', False)
    scan_way = kwargs.get('scan_way', 1)
    version = kwargs.get('version', '')

    if not all((app_id, group_id)):
        raise ParameterIsEmptyException('"app_id, group_id" parameters cannot be empty.')

    app_obj = get_app_by_id(app_id=app_id)
    group_obj = get_t_group_by_id(group_id=group_id)

    task = create_task_obj(
        app_obj=app_obj,
        group_obj=group_obj,
        is_force_scan=is_force_scan,
        scan_way=scan_way,
        version=version,
    )

    return task


def create_task_by_project(**kwargs):
    """

    :param kwargs:
    :return:
    """
    project_id = kwargs.get('project_id', None)
    branch = kwargs.get('branch', None)
    group_id = kwargs.get('group_id', None)
    is_force_scan = kwargs.get('is_force_scan', False)
    scan_way = kwargs.get('scan_way', 1)
    version = kwargs.get('version', '')

    if not all((project_id, branch, group_id)):
        raise ParameterIsEmptyException('"project_id, branch, group_id" parameters cannot be empty.')

    project_obj = get_project_by_id(project_id=project_id)
    repo_obj = get_repository_by_name(name=branch.strip(), project_id=project_obj.id)

    # FIXME verify project_obj, profile_obj is not None

    if not repo_obj:
        raise NotFoundBranchException('"{0}" branch not found.'.format(branch))

    app_obj = get_app_by_branch(name=branch, project_id=project_id)

    if not app_obj:  # create application
        app_obj = create_app_obj(
            project_obj=project_obj,
            module_name=branch,
            app_name=branch,
            repo_obj=repo_obj,

        )

    task = create_task_obj(
        app_obj=app_obj,
        scan_way=scan_way,
        is_force_scan=is_force_scan,
        version=version,
    )
    return task


def _get_task_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    task_id = kwargs.get('task_id', None)
    app_id = kwargs.get('app_id', None)
    status = kwargs.get('status', None)
    close_old_connections()

    try:
        sql_where = {}
        if task_id:
            sql_where['id'] = int(task_id)
        if app_id:
            sql_where["app__id"] = int(app_id)
        if status:
            sql_where["status__in"] = status
        if not sql_where:
            raise QueryConditionIsEmptyException(u'Missing "task_id" key parameters!')

        item = TaskInfo.objects.filter(**sql_where).first()
        return item
    except TaskInfo.DoesNotExist as ex:
        logger.warn(ex)
        return None


def update_task_obj(**kwargs):
    """
    获取资产
    :param kwargs:
    :return:
    """
    task_id = kwargs.get('task_id', None)
    log_file = kwargs.get('log_file', None)
    executor_ip = kwargs.get('executor_ip', None)
    status = kwargs.get('status', None)
    start_time = kwargs.get('start_time', None)
    end_time = kwargs.get('end_time', None)
    config = kwargs.get('config', None)
    reason = kwargs.get('reason', None)
    title = kwargs.get('title', None)
    commit_hash = kwargs.get('commit_hash', None)
    critical = kwargs.get("critical", None)
    high = kwargs.get("high", None)
    medium = kwargs.get("medium", None)
    low = kwargs.get("low", None)
    info = kwargs.get("info", None)
    scope = kwargs.get("scope", None)
    level = kwargs.get("level", None)
    log_path = kwargs.get('log_path', '')
    scan_template = kwargs.get('scan_template', '')
    scan_template_version = kwargs.get('scan_template_version', '')
    close_old_connections()

    try:
        sql_where = {}

        if task_id:
            sql_where['id'] = int(task_id)
        if not sql_where:
            raise QueryConditionIsEmptyException(u'Missing "task_id" key parameters!')

        item = TaskInfo.objects.get(**sql_where)
        if item:
            if log_file:
                item.log_file = log_file
            if executor_ip:
                item.executor_ip = executor_ip
            if scan_template:
                item.template_name = scan_template
            if scan_template_version:
                item.template_version = scan_template_version

            # FIXME 强关联状态，不允许逆修改
            if status:
                item.status = int(status)
            if config:
                item.config = config

            item.error_reason = reason
            if title:
                title = title[:255]
            item.error_title = title
            if start_time:
                item.start_time = start_time
            if item.start_time and end_time:
                item.end_time = end_time
                update_app_obj(
                    app_id=item.app.id,
                    last_scan_time=end_time
                )
            if commit_hash:
                item.hash = commit_hash
            if critical or critical == 0:
                item.critical = int(critical)
            if high or high == 0:
                item.high = int(high)
            if medium or medium == 0:
                item.medium = int(medium)
            if low or low == 0:
                item.low = int(low)
            if info or info == 0:
                item.info = int(info)
            if log_path:
                item.log_file = log_path

            if item.status == 6:
                update_app_statistics(
                    app_id=item.app.id,
                    critical=critical,
                    high=high,
                    medium=medium,
                    low=low,
                    info=info,
                    scope=scope,
                )

            item.save(level=level)
            cache.set('{0}:{1}'.format(SCAN_CACHE[3], task_id), None, 0)
        return item
    except TaskInfo.DoesNotExist as ex:
        logger.warn(ex)
        return None


def update_task_config(task_id, config):
    """

    :param task_id:
    :param config:
    :return:
    """
    return update_task_obj(
        task_id=task_id,
        config=config,
        title="更新扫描任务配置信息"
    )


def update_task_scan_init(**kwargs):
    """

    :param kwargs:
    :return:
    """
    task_id = kwargs.get('task_id', None)
    scan_template = kwargs.get('scan_template', '')
    scan_template_version = kwargs.get('scan_template_version', '')
    executor_ip = kwargs.get('executor_ip', '')
    title = kwargs.get('title', '')
    reason = kwargs.get('reason', '')
    log_path = kwargs.get('log_path', '')
    start_time = kwargs.get('start_time', datetime.datetime.now())

    return update_task_obj(
        task_id=task_id,
        status=3,
        executor_ip=executor_ip,
        scan_template=scan_template,
        scan_template_version=scan_template_version,
        reason=reason,
        title=title,
        log_path=log_path,
        start_time=start_time
    )


def update_task_scan_component(**kwargs):
    """

    :param kwargs:
    :return:
    """
    task_id = kwargs.get('task_id', None)
    executor_ip = kwargs.get('executor_ip', '')
    commit_hash = kwargs.get('commit_hash', '')
    title = kwargs.get('title', '')
    reason = kwargs.get('reason', '')

    return update_task_obj(
        task_id=task_id,
        status=4,
        commit_hash=commit_hash,
        executor_ip=executor_ip,
        reason=reason,
        title=title,
    )


def update_task_start(**kwargs):
    """

    :param kwargs:
    :return:
    """
    task_id = kwargs.get('task_id', None)
    executor_ip = kwargs.get('executor_ip', '')
    title = kwargs.get('title', '')
    reason = kwargs.get('reason', '')

    return update_task_obj(
        task_id=task_id,
        status=5,
        executor_ip=executor_ip,
        reason=reason,
        title=title,
    )


def update_task_success(**kwargs):
    """

    :param kwargs:
    :return:
    """
    task_id = kwargs.get("task_id")
    title = kwargs.get("title")
    log_path = kwargs.get("log_path")
    end_time = kwargs.get("end_time", datetime.datetime.now())

    return update_task_obj(
        task_id=task_id,
        status=6,
        title=title,
        log_path=log_path,
        end_time=end_time
    )


def update_task_title(**kwargs):
    """

    :param kwargs:
    :return:
    """
    task_id = kwargs.get("task_id")
    title = kwargs.get("title")
    reason = kwargs.get("reason")
    level = kwargs.get("level", 4)

    return update_task_obj(
        task_id=task_id,
        title=title,
        reason=reason,
        level=level,
    )


def update_task_statistics(**kwargs):
    """

    :param kwargs:
    :return:
    """
    task_id = kwargs.get("task_id")
    critical = kwargs.get("critical")
    high = kwargs.get("high")
    medium = kwargs.get("medium")
    low = kwargs.get("low")
    info = kwargs.get("info")
    scope = kwargs.get("scope")
    title = kwargs.get('title', '')
    reason = kwargs.get('reason', '')

    return update_task_obj(
        task_id=task_id,
        critical=critical,
        high=high,
        medium=medium,
        low=low,
        info=info,
        title=title,
        reason=reason,
        scope=scope,
    )


def update_task_failed(**kwargs):
    """

    :param kwargs:
    :return:
    """
    task_id = kwargs.get("task_id")
    title = kwargs.get("title")
    reason = kwargs.get("reason")
    end_time = kwargs.get("end_time", datetime.datetime.now())

    return update_task_obj(
        task_id=task_id,
        status=1,
        end_time=end_time,
        title=title,
        reason=reason,
        level=2,
    )


def get_task_by_id(task_id):
    """

    :param task_id:
    :return:
    """
    cache_key = '{0}:{1}'.format(SCAN_CACHE[3], task_id)
    cache_obj = cache.get(cache_key)
    if cache_obj:
        return cache_obj
    obj = _get_task_obj(task_id=task_id)
    if obj:
        cache.set(cache_key, obj, SCAN_CACHE[0])
    return obj


def delete_by_list(t_list):
    """

    :return:
    """
    task_list = TaskInfo.objects.filter(id__in=t_list)
    for item in task_list:
        cache_key = '{0}:{1}'.format(SCAN_CACHE[3], item.id)
        cache.set(cache_key, None, 0)
        item.delete()
    # TODO 检测是否有任务在执行
