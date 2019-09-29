# coding: utf-8
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie

from seecode.apps.node.models import HostInfo
from seecode.libs.core.enum import NODE_ROLE_TYPE
from seecode.libs.paginator import Paginator
from seecode.libs.units import parse_int


@login_required
@ensure_csrf_cookie
def index(request):
    """
    :param request:
    :return:
    """
    cate = request.GET.get('c', '')
    keyword = request.GET.get('k', '')

    page_num = parse_int(request.GET.get('p', 1), 1)
    page_size = parse_int(request.GET.get('ps', 20), 20)

    sql_where = {}

    if cate:
        sql_where['origin__id'] = int(cate)

    items = HostInfo.objects.filter(**sql_where).order_by('-created_at')
    paginator = Paginator(items, page_size, request=request, pre_name=u"节点")
    page = paginator.page(page_num)

    return render(request, 'node/host/index.html', {
        'nav': 'node',
        'page': page,
        'keyword': keyword,
        'node_role': NODE_ROLE_TYPE,
    })


@login_required
@ensure_csrf_cookie
def show(request, node_id):
    """
    :param request:
    :param node_id:
    :return:
    """
    try:
        model = HostInfo.objects.get(id=node_id)

    except HostInfo.DoesNotExist as ex:
        model = None

    return render(request, 'node/host/edit.html', {
        'nav': 'node',
        'model': model,
    })

