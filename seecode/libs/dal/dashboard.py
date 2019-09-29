# coding: utf-8
from __future__ import unicode_literals
import datetime
from django.core.cache import cache
from collections import OrderedDict

from seecode.apps.project.models.app import ApplicationInfo
from seecode.apps.project.models.item import ProjectInfo
from seecode.apps.project.models.group import GroupInfo
from seecode.apps.project.models.member import MemberInfo
from seecode.apps.scan.models import TaskInfo
from seecode.apps.scan.models import IssueInfo
from seecode.libs.core.cache_key import DASHBOARD


def _get_dashboard_total():
    """

    :return:
    """
    cache_obj = cache.get(DASHBOARD[1])
    if cache_obj:
        return cache_obj
    result = {
        'project_group_count': 0,
        'project_count': 0,
        'user_count': 0,
        'app_count': 0,
    }
    result['project_group_count'] = GroupInfo.objects.filter().count()
    result['project_count'] = ProjectInfo.objects.filter().count()
    result['user_count'] = MemberInfo.objects.filter(state='active').count()
    result['app_count'] = ApplicationInfo.objects.filter().count()
    if result:
        cache.set(DASHBOARD[1], result, DASHBOARD[0])
    return result


def _get_recent_project(day=15):
    """
    项目趋势
    :return:
    """
    cache_obj = cache.get(DASHBOARD[3])
    if cache_obj:
        return cache_obj
    result = {}
    for i in range(0, day):
        start_time = datetime.datetime.now() + datetime.timedelta(days=int(-i))
        s_time = '{0} 00:00:00'.format(start_time.strftime('%Y-%m-%d'))
        e_time = '{0} 23:59:59'.format(start_time.strftime('%Y-%m-%d'))
        activity = ProjectInfo.objects.filter(git_last_activity_at__gte=s_time, git_last_activity_at__lte=e_time).count()
        new = ProjectInfo.objects.filter(created_at__gte=s_time, created_at__lte=e_time).count()
        result[start_time.strftime('%Y-%m-%d')] = {
            'activity': activity,
            'new': new,
        }
    result = OrderedDict(sorted(result.items(), key=lambda kv: kv[0]))
    cache.set(DASHBOARD[3], result, DASHBOARD[0])
    return result


def _get_recent_scan(day=15):
    """
    最近扫描
    :return:
    """
    result = {}

    return result


def _get_current_month_bu_scan(top=10):
    """
    本月部门扫描排名 TOP 10
    :return:
    """

    result = {}


    return result


def _get_tactic_type():
    """
    本月部门扫描排名 TOP 10
    :return:
    """
    result = {
        'Code Smell': 0,
        'Bug': 0,
        'Vulnerability': 0,
    }

    return result


def _get_24h_issue_alarm(limit=24):
    """
    告警
    :return:
    """
    result = []
    return result


def get_dashboard_statistics():
    """

    :return:
    """
    result = {
        'total': _get_dashboard_total(),
        'recent_scan': _get_recent_scan(),
        'recent_project': _get_recent_project(),
        'current_month_bu': _get_current_month_bu_scan(),
        'tactic_type': _get_tactic_type(),
        'issues_alarm': _get_24h_issue_alarm(),
    }
    return result
