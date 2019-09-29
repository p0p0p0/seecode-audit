# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.cache import cache

from seecode import __version__
from seecode.apps.system.models import SyslogInfo
from seecode.libs.core.cache_key import SYSTEM_CACHE
from seecode.libs.dal.dashboard import get_dashboard_statistics
from seecode.libs.utils.perm import PermWrapper

PER_CACHE_KEY = 'perm'


def permission_settings(request):
    """
    全局变量
    :param request:
    :return:
    """

    perm = PermWrapper(request.user)
    cache_key = '{0}:{1}'.format(PER_CACHE_KEY, request.user.id)
    result = cache.get(cache_key)
    user_best_group = ''

    if not result:
        perm = PermWrapper(request.user)
        request.session['perm'] = perm.perm_list
        user_best_group = None
        groups = request.user.groups.all()
        for group in groups:
            if group.id == 3:
                user_best_group = group
                break
            user_best_group = group

        result = {
            'perm': perm,
            'user_best_group': user_best_group,
            'version': __version__,
            'syslogs': [],
            'syslog_count': 0
        }

        cache.set(cache_key, result, 60 * 15)

    request.session['perm'] = perm.perm_list
    syslogs = cache.get(SYSTEM_CACHE[7])
    if not syslogs:
        syslogs = SyslogInfo.objects.filter(
            type=1,
            is_read=False,
            level__in=[1]
        ).order_by('-created_at')[:10]

        cache.set(SYSTEM_CACHE[7], syslogs, 60 * 5)
    dashboard = get_dashboard_statistics()

    return {
        'perm': perm,
        'version': __version__,
        'syslogs': syslogs,
        'syslogs_count': 0,
        'user_best_group': user_best_group,
        'dashboard': dashboard
    }
