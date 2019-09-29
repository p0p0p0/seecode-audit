# coding: utf-8
from __future__ import unicode_literals

import codecs
import json
import uuid

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.http import urlquote
from django.views.decorators.csrf import ensure_csrf_cookie

from seecode.apps.node.models import ServiceInfo
from seecode.libs.core.enum import NODE_ROLE_TYPE
from seecode.libs.dal.engine import get_all_engine
from seecode.libs.dal.service import create_service_obj
from seecode.libs.paginator import Paginator
from seecode.libs.units import parse_int


@login_required
@ensure_csrf_cookie
def index(request):
    """
    :param request:
    :return:
    """
    if request.method == "POST":
        try:
            save(request)
            name = request.POST.get('name', '')
            msg = urlquote(' "{0}" 服务注册成功!'.format(name))
            return HttpResponseRedirect('/node/service/?msg={0}'.format(msg))
        except Exception as ex:
            import traceback;
            traceback.print_exc()
            return HttpResponseRedirect('/node/service/?errmsg={0}'.format(urlquote(str(ex))))
    else:
        action = request.GET.get('action', '')
        if action:
            items = ServiceInfo.objects.all()
            services = []
            for item in items:
                services.append({
                    'name': item.name,
                    'key': item.key,
                    'role': 'ui' if item.role == 1 else 'client',
                    'keyword': item.process_keyword
                })
            response = HttpResponse(json.dumps(services, indent=2), content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="services.json"'
            response.write(codecs.BOM_UTF8)
            return response

        else:
            keyword = request.GET.get('k', '')
            page_num = parse_int(request.GET.get('p', 1), 1)
            page_size = parse_int(request.GET.get('ps', 20), 20)
            sql_where = {}
            if keyword:
                sql_where['name__icontains'] = keyword.strip()

            items = ServiceInfo.objects.filter(**sql_where).order_by('-created_at')
            paginator = Paginator(items, page_size, request=request, pre_name=u"服务")
            page = paginator.page(page_num)

            return render(request, 'node/service/index.html', {
                'nav': 'node',
                'page': page,
                'keyword': keyword,
                'engines': get_all_engine(),
                'node_role': NODE_ROLE_TYPE,
            })


@login_required
def save(request):
    """
    :param request:
    :return:
    """
    result = None
    name = request.POST.get('name', '')
    process_keyword = request.POST.get('process_keyword', '')
    role = request.POST.get('role', '')
    description = request.POST.get('description', '')

    if not all((name, process_keyword)):
        raise Exception('"name, process_keyword" 参数不能为空!')

    service_obj = create_service_obj(
        name=name,
        process_keyword=process_keyword,
        role=role,
        description=description,
        key=uuid.uuid4().hex
    )
