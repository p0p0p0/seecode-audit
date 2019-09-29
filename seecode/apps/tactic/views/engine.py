# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import ast

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie

from seecode.apps.tactic.models import EngineInfo
from seecode.libs.dal.engine import get_engine_by_id
from seecode.libs.dal.engine import update_engine_obj
from seecode.libs.paginator import Paginator
from seecode.libs.units import parse_int


@login_required
@ensure_csrf_cookie
def index(request):
    """
    :param request:
    :return:
    """
    keyword = request.GET.get('k', '')

    page_num = parse_int(request.GET.get('p', 1), 1)
    page_size = parse_int(request.GET.get('ps', 20), 20)

    sql_where = {}

    if keyword:
        keyword = keyword.strip()
        sql_where['name__icontains'] = keyword

    items = EngineInfo.objects.filter(**sql_where).order_by('-created_at')
    paginator = Paginator(items, page_size, request=request, pre_name=u"引擎")
    page = paginator.page(page_num)

    return render(request, 'tactic/engine/index.html', {
        'nav': 'tactic',
        'page': page,
        'keyword': keyword,
    })


@login_required
@ensure_csrf_cookie
def edit(request, engine_id):
    """
    :param request:
    :param engine_id:
    :return:
    """
    model = get_engine_by_id(engine_id=engine_id)
    if not model:
        raise Exception('扫描模板未找到!')
    if request.method == 'POST':
        description = request.POST.get('description', '')
        key_list = request.POST.getlist('key', '')
        value_list = request.POST.getlist('value', '')
        update_engine_obj(
            description=description,
            key_list=key_list,
            value_list=value_list,
            engine_id=engine_id
        )
        return HttpResponseRedirect("/tactic/engine/{0}/".format(engine_id))
    else:
        return render(request, 'tactic/engine/edit.html', {
            'nav': 'tactic',
            'model': model,
            'paramters': ast.literal_eval(model.config or '{}'),
        })
