# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import time

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django_celery_beat.models import PeriodicTask, PeriodicTasks, IntervalSchedule, CrontabSchedule

from seecode.libs.paginator import Paginator
from seecode.libs.units import parse_int, handle_uploaded_file, perm_verify


@login_required
@ensure_csrf_cookie
@perm_verify(['system.view_employeeinfo'])
def index(request):
    """
    :param request:
    :return:
    """

    title = request.GET.get('t', '')
    level = request.GET.get('l', '')

    page_num = parse_int(request.GET.get('p', 1), 1)
    page_size = parse_int(request.GET.get('ps', 20), 20)

    sql_where = {
        'id__gt':1
    }

    if title:
        sql_where['name__icontains'] = title
    if level:
        sql_where['level'] = int(level)

    items = PeriodicTask.objects.filter(**sql_where).order_by('-date_changed')
    paginator = Paginator(items, page_size, request=request, pre_name=u"服务")
    page = paginator.page(page_num)

    return render(request, 'system/service/index.html', {
        'nav': 'sys',
        'page': page,
        'level': level,
        'title': title,

    })


@login_required
@ensure_csrf_cookie
@perm_verify(['system.view_employeeinfo'])
def show(request, s_id):
    """
    :param request:
    :param s_id:
    :return:
    """
    model = PeriodicTask.objects.filter(id=s_id).first()
    if request.method == 'POST':
        sched = request.POST.get('sched_list', '')
        model.crontab = CrontabSchedule.objects.filter(id=sched).first()
        model.save()
        return  HttpResponseRedirect("/sys/service/")
    else:
        sched_list = CrontabSchedule.objects.filter()

        return render(request, 'system/service/edit.html', {
            'nav': 'sys',
            'model': model,
            'sched_list': sched_list,

        })


