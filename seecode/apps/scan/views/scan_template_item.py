# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie

from seecode.apps.scan.models import ScanProfileInfo
from seecode.apps.tactic.models import TacticInfo
from seecode.libs.core.enum import RISK_TYPE
from seecode.libs.core.enum import TACTIC_TYPE
from seecode.libs.core.enum import action as changelog_action
from seecode.libs.core.enum import changelog_module
from seecode.libs.dal.engine import get_all_customize_engine
from seecode.libs.dal.upgrade_version import update_client_revision_version
from seecode.libs.paginator import Paginator
from seecode.libs.units import parse_int


@login_required
@ensure_csrf_cookie
def index(request, template_id):
    """
    :param request:
    :param template_id:
    :return:
    """
    model = ScanProfileInfo.objects.filter(id=template_id).first()
    if request.method == "POST":
        save(request, model)
        return HttpResponseRedirect('/scan/template/{0}/tactics/'.format(template_id))
    else:
        risk = request.GET.get('r', '')
        nature_type = request.GET.get('n', '')
        engine = request.GET.get('e', '')
        cate = request.GET.get('c', '')
        keyword = request.GET.get('k', '')
        page_num = parse_int(request.GET.get('p', 1), 1)
        page_size = parse_int(request.GET.get('ps', 20), 20)
        sql_where = {}

        if risk:
            sql_where['risk'] = int(risk)
        if engine:
            sql_where['engine__id'] = int(engine)
        else:
            if model.engines.all():
                sql_where['engine__id__in'] = [_.id for _ in model.engines.all()]
        if cate:
            sql_where['type'] = int(cate)
        if nature_type:
            sql_where['nature_type'] = nature_type
        if keyword:
            sql_where['name__icontains'] = keyword.strip()

        items = TacticInfo.objects.filter(**sql_where).order_by("-created_at")
        engine_ids = get_all_customize_engine()

        paginator = Paginator(items, page_size, request=request, pre_name=u"扫描策略")
        page = paginator.page(page_num)

        return render(request, 'scan/template/items/index.html', {
            'nav': 'scan',
            'page': page,
            'keyword': keyword,
            'e': engine,
            'c': cate,
            'r': risk,
            'n': nature_type,
            'model': model,
            'risk_list': RISK_TYPE,
            'tactics': TACTIC_TYPE,
            'rule_list': TacticInfo.objects.filter(engine__id__in=[_.id for _ in engine_ids]),
        })


@login_required
def save(request, model):
    """

    :param request:
    :param model:
    :return:
    """
    result = {'status': 1, 'msg': ''}
    action = request.POST.get('action', '')
    ids = request.POST.get('ids', '')
    try:
        if action == 'del':
            items = TacticInfo.objects.filter(id__in=[_ for _ in ids.split(',') if _])
            model.tactics.remove(*items)
            msg = '删除“{0}”模板添加 {1} 条扫描策略\n'.format(model, items.count())
            update_client_revision_version(
                action=changelog_action.DEL,
                module=changelog_module.SCAN_TEMPLATE,
                description=msg
            )

        else:
            items = TacticInfo.objects.filter(id__in=[_ for _ in ids.split(',') if _])
            model.tactics.add(*items)
            msg = '添加 “{0}”模板添加 {1} 条扫描策略\n'.format(model, items.count())
            update_client_revision_version(
                action=changelog_action.ADD,
                module=changelog_module.SCAN_TEMPLATE,
                description=msg
            )
        result['status'] = 1
        result['msg'] = '成功'
    except Exception as ex:
        import traceback;
        traceback
        result = {'status': -1, 'msg': str(ex)}

    return JsonResponse(result, safe=False)
