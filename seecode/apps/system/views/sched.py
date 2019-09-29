# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.http import urlquote
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django_celery_beat.models import CrontabSchedule, IntervalSchedule, PeriodicTask

from seecode.libs.paginator import Paginator
from seecode.apps.system.models import SchedInfo
from seecode.libs.dal.sched import create_sched_obj, get_trigger_by_cron_id, get_trigger_by_interval_id
from seecode.libs.core.enum import SCHED_TYPE
from seecode.libs.units import parse_int, handle_uploaded_file, perm_verify


@login_required
@ensure_csrf_cookie
@perm_verify(['system.view_employeeinfo'])
def index(request):
    """
    :param request:
    :return:
    """
    if request.method == 'POST':
        try:
            action = request.POST.get('action', 'add')
            if action == 'add':
                save(request)
                return HttpResponseRedirect('/sys/service/sched/?msg={0}'.format(urlquote('创建成功!')))
            elif action == 'del':
                delete(request)
                return HttpResponseRedirect('/sys/service/sched/?msg={0}'.format(urlquote('删除成功!')))
            else:
                return HttpResponseRedirect('/sys/service/sched/')
        except Exception as ex:
            import traceback;traceback.print_exc()
            return HttpResponseRedirect('/sys/service/sched/?errmsg={0}'.format(urlquote(str(ex))))
    else:
        title = request.GET.get('k', '')
        level = request.GET.get('l', '')

        page_num = parse_int(request.GET.get('p', 1), 1)
        page_size = parse_int(request.GET.get('ps', 20), 20)
        sql_where = {}
        if title:
            sql_where['name__icontains'] = title.strip()
        if level:
            sql_where['level'] = int(level)

        items = SchedInfo.objects.filter(**sql_where).order_by('-created_at')
        paginator = Paginator(items, page_size, request=request, pre_name=u"定时器")
        page = paginator.page(page_num)

        return render(request, 'system/service/sched/index.html', {
            'nav': 'sys',
            'page': page,
            'level': level,
            'keyword': title,
            'sched_list': SCHED_TYPE,

        })


@login_required
@perm_verify(['auth.change_permission', 'auth.add_permission'])
def save(request):
    """
    :param request:
    :return:
    """
    sched_type = request.POST.get('type', '')
    name = request.POST.get('name', '')
    value = request.POST.get('value', '')
    sched_id = request.POST.get('sched_id', '')

    if sched_id:
        pass
    else:
        create_sched_obj(
            name=name,
            type=sched_type,
            value=value,
        )


@login_required
@perm_verify(['auth.change_permission', 'auth.add_permission'])
def delete(request):
    """
    :param request:
    :return:
    """
    ids = request.POST.get('ids', '')

    items = SchedInfo.objects.filter(id__in=[_ for _ in ids.split(',') if _])
    for item in items:
        CrontabSchedule.objects.filter(id=item.crontab.id).delete()
        item.delete()

