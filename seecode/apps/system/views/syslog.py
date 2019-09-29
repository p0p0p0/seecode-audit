# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie

from seecode.libs.core.cache_key import SYSTEM_CACHE
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from django.core.cache import cache


from seecode.apps.system.models import SyslogInfo
from seecode.libs.paginator import Paginator
from seecode.libs.units import parse_int
from seecode.libs.core.enum import SYSLOG_LEVEL


@login_required
@ensure_csrf_cookie
def index(request):
    """
    :param request:
    :return:
    """
    level = request.GET.get('l', '')
    read = request.GET.get('r', '')
    keyword = request.GET.get('k', '')
    object_id = request.GET.get('o', '')
    page_num = parse_int(request.GET.get('p', 1), 1)
    page_size = parse_int(request.GET.get('ps', 15), 15)
    modules = []  #ContentType.objects.filter(id__in=[1,2,3,4,5,6,7,8,9,11,12])

    sql_where = {}
    if object_id:
        sql_where['object_id'] = object_id.strip()
    if keyword:
        keyword = keyword.strip()
        sql_where['title__icontains'] = keyword
    if level:
        sql_where['level'] = int(level)
    if read == '2':
        sql_where['is_read'] = False
    elif read == '1':
        sql_where['is_read'] = True

    items = SyslogInfo.objects.filter(**sql_where).order_by('-created_at')
    paginator = Paginator(items, page_size, request=request, pre_name=u"日志")
    page = paginator.page(page_num)

    return render(request, 'system/syslog/index.html', {
        'nav': 'sys',
        'page': page,
        'k': keyword,
        'l': level,
        'r': read,
        'obj_str': object_id,
        'levels': SYSLOG_LEVEL,
        'modules': modules,
    })


@login_required
@ensure_csrf_cookie
def show(request, syslog_id):
    """

    :param request:
    :param syslog_id:
    :return:
    """
    model = None
    try:
        model = SyslogInfo.objects.get(id=syslog_id)
        model.is_read = True
        model.save()
        cache.set(SYSTEM_CACHE[7], None, 0)
    except Exception as ex:
        pass

    return render(request, 'system/syslog/show.html', {
        'nav': 'sys',
        'model': model,
    })


@login_required
@ensure_csrf_cookie
def batch(request):
    """

    :param request:
    :return:
    """
    action = request.POST.get('action', '')
    ids = request.POST.get('ids', '')

    try:
        if action == 'del':
            limit_date = datetime.datetime.now() - datetime.timedelta(days=180)
            SyslogInfo.objects.filter(created_at__lte=limit_date).delete()
        elif action == 'read':
            SyslogInfo.objects.filter(id__in=[i for i in ids.split(',') if i]).update(is_read=True)
    except Exception as ex:
        import traceback;traceback.print_exc()
        raise ex

    return JsonResponse({"status": "ok"}, safe=True)
