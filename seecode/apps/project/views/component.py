# coding: utf-8
from __future__ import unicode_literals

import codecs
import csv

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from pytz import timezone

from seecode.apps.project.models.app import DependentInfo
from seecode.libs.dal.application import get_app_by_id
from seecode.libs.dal.gitlab_project import get_project_by_id
from seecode.libs.paginator import Paginator
from seecode.libs.units import parse_int
from seecode.libs.core.common import get_dork_query


@login_required
@ensure_csrf_cookie
def index(request):
    """
    :param request:
    :return:
    """
    pro_id = request.GET.get('pro', '')
    app_id = request.GET.get('a', '')
    keyword = request.GET.get('k', '')
    archive = request.GET.get('archive', '')
    dork_query = get_dork_query(keyword)

    page_num = parse_int(request.GET.get('p', 1), 1)
    page_size = parse_int(request.GET.get('ps', 20), 20)

    sql_where = {
        'is_archive': False
    }
    project_obj = None
    app_obj = None

    if pro_id:
        sql_where['app__project__id'] = int(pro_id)
        project_obj = get_project_by_id(pro_id)
    if app_id:
        sql_where['app__id'] = int(app_id)
        app_obj = get_app_by_id(app_id)
    if keyword:
        if dork_query['data']:
            for q, k in dork_query['data'].items():
                if q == 'name':
                    sql_where['name'] = k
                elif q == 'group':
                    sql_where['group_id'] = k
                elif q == 'origin':
                    sql_where['file_name__icontains'] = k
        else:
            keyword = keyword.strip()
            sql_where['name__icontains'] = keyword
    if archive == '1':
        sql_where['is_archive'] = True

    items = DependentInfo.objects.filter(**sql_where).order_by('-created_at')
    paginator = Paginator(items, page_size, request=request, pre_name=u"组件")
    page = paginator.page(page_num)

    return render(request, 'project/component/index.html', {
        'nav': 'pro',
        'page': page,
        'keyword': keyword,
        'project_obj': project_obj,
        'app_obj': app_obj,
        'archive': archive,
    })


@login_required
@ensure_csrf_cookie
def export(request):
    """
    :param request:
    :return:
    """
    pro_id = request.GET.get('pro', '')
    app_id = request.GET.get('a', '')
    keyword = request.GET.get('k', '')
    archive = request.GET.get('archive', '')
    sql_where = {
        'is_archive': False
    }
    if pro_id:
        sql_where['app__project__id'] = int(pro_id)
    if app_id:
        sql_where['app__id'] = int(app_id)
    if keyword:
        keyword = keyword.strip()
        sql_where['name__icontains'] = keyword
    if archive == '1':
        sql_where['is_archive'] = True

    items = DependentInfo.objects.filter(**sql_where).order_by('-created_at')
    tz = timezone(settings.TIME_ZONE)
    response = HttpResponse(content_type='text/csv')
    response.write(codecs.BOM_UTF8)
    response['Content-Disposition'] = 'attachment; filename="component.csv"'

    writer = csv.writer(response)
    # name, tag, version, module.name, module.project.name, module.git_url
    writer.writerow([u'组件名称', u'groupId', u'版本', u'文件位置', u'分支名称', u'项目名称', u'项目地址', '发现时间'])

    if items:
        for item in items:
            try:
                row = [
                    item.name,
                    item.group_id,
                    item.version,
                    item.file_name,
                    item.app.repo,
                    item.app.project,
                    item.app.project.web_url,
                    item.created_at.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S"),
                ]
                writer.writerow(row)
            except Exception as ex:
                pass

    return response
