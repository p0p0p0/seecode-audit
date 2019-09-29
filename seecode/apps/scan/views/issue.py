# coding: utf-8
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie

from seecode.apps.scan.models import IssueFlowInfo
from seecode.apps.scan.models import IssueInfo
from seecode.libs.core.enum import ISSUE_STATUS
from seecode.libs.core.enum import RISK_TYPE
from seecode.libs.core.enum import TACTIC_TYPE
from seecode.libs.dal.application import get_app_by_id
from seecode.libs.dal.engine import get_all_engine
from seecode.libs.dal.issue import update_issue_obj
from seecode.libs.dal.scan_task import get_task_by_id
from seecode.libs.dal.tactic import get_tactic_tags_by_id
from seecode.libs.paginator import Paginator
from seecode.libs.units import parse_int
from seecode.libs.units import strip


@login_required
@ensure_csrf_cookie
def index(request, task_id=None):
    """
    :param request:
    :param task_id:
    :return:
    """
    app_id = strip(request.GET.get('app', ''))
    e = strip(request.GET.get('e', ''))
    cate = strip(request.GET.get('c', ''))
    risk = strip(request.GET.get('r', ''))
    done = strip(request.GET.get('d', ''))
    keyword = request.GET.get('k', '')
    a = request.GET.get('a', '')

    page_num = parse_int(request.GET.get('p', 1), 1)
    page_size = parse_int(request.GET.get('ps', 20), 20)
    sql_where = {}
    app_obj = None

    if task_id:
        task = get_task_by_id(task_id)
        if task:
            app_obj = get_app_by_id(task.app.id)
            sql_where['app__id'] = task.app.id
    if app_id:
        app_obj = get_app_by_id(app_id)
        sql_where['app__id'] = app_id
    if e:
        sql_where['tactic__engine__id'] = int(e)
    if risk:
        sql_where['tactic__risk'] = risk
    if cate:
        sql_where['tactic__type'] = int(cate)
    if keyword:
        keyword = keyword.strip()
        sql_where['title__icontains'] = keyword
    if a:
        if a == '1':
            sql_where['is_send_alarm'] = True
        elif a == '2':
            sql_where['scm_url__isnull'] = False
    if done:
        if done == '1':
            sql_where['status__in'] = [2, 3, 4, 5]
        elif done == '2':
            sql_where['status'] = 1
        elif done == '3':
            sql_where['is_false_positive'] = True

    items = IssueInfo.objects.filter(**sql_where).order_by("-updated_at")
    paginator = Paginator(items, page_size, request=request, pre_name=u"问题")
    page = paginator.page(page_num)

    return render(request, 'scan/issue/index.html', {
        'nav': 'scan',
        'page': page,
        'e': e,
        'c': cate,
        'r': risk,
        'd': done,
        'alarm': a,
        'app_obj': app_obj,
        'keyword': keyword,
        'issues_type': TACTIC_TYPE,
        'risk_list': RISK_TYPE,
        'engine_list': get_all_engine(),
        'issues_status': ISSUE_STATUS,
    })


@login_required
@ensure_csrf_cookie
def show(request, issue_id):
    """
    :param request:
    :param issue_id:
    :return:
    """
    if request.method == 'POST':
        role = strip(request.POST.get('role', ''))
        title = strip(request.POST.get('title', ''))
        status = strip(request.POST.get('status', ''))
        comment = strip(request.POST.get('comment', ''))
        if role == 'title':
            update_issue_obj(
                issue_id=issue_id,
                title=title
            )
        elif role == 'status':
            update_issue_obj(
                issue_id=issue_id,
                status=status,
                comment=comment,
                user=request.user,
            )
        return HttpResponseRedirect('/scan/issue/{0}/'.format(issue_id))
    else:
        code_segment, issue_flows, tags = [], [], []
        try:
            model = IssueInfo.objects.get(id=issue_id)
            code_segment_list = model.code_segment.split('\n')
            if model.start_line == 1:
                i = 0
            else:
                i = -1
            for code in code_segment_list:
                code_safe = code.replace("<", "&lt;")
                code_safe = code_safe.replace(">", "&gt;")
                if model.start_line+i == model.start_line:
                    code_segment.append("<i style='color:#c0c0c0'>{0}.</i> <span id='element' style='font-weight: bold;"
                                        "color:purple; background-color:#ccc'>{1}</span>".format(model.start_line+i, code_safe))
                else:
                    code_segment.append("<i style='color:#c0c0c0'>{0}.</i> "
                                        "<span style='color:blue'>{1}</span>".format(model.start_line+i, code_safe))
                i += 1
            issue_flows = IssueFlowInfo.objects.filter(issue__id=model.id).order_by("created_at")

            tags = get_tactic_tags_by_id(tactic_id=model.tactic.id)

        except IssueInfo.DoesNotExist as ex:
            model = None

        return render(request, 'scan/issue/show.html', {
            'nav': 'scan',
            'issue_status': ISSUE_STATUS,
            'model': model,
            'code_segment': '\n'.join(code_segment),
            'issue_flows': issue_flows,
            'tags': tags,
        })
