# coding: utf-8
from __future__ import unicode_literals

import os
import uuid

import markdown
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie

from seecode.apps.node.models import UpgradePackageInfo
from seecode.libs.core.enum import NODE_ROLE_TYPE
from seecode.libs.dal.engine import get_all_engine
from seecode.libs.dal.service import create_service_obj
from seecode.libs.dal.upgrade_package import create_package_obj
from seecode.libs.dal.upgrade_version import get_current_client_version
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
        # make upgrade package
        action = request.POST.get('action', '')
        if action == 'release':
            description = request.POST.get('description', '')
            create_package_obj(description=description)
        elif action == 'archive':
            archive(request)
        return HttpResponseRedirect('/node/upgrade/')
    else:
        keyword = request.GET.get('k', '')
        page_num = parse_int(request.GET.get('p', 1), 1)
        page_size = parse_int(request.GET.get('ps', 20), 20)
        sql_where = {}
        if keyword:
            sql_where['name__icontains'] = keyword.strip()

        items = UpgradePackageInfo.objects.filter(**sql_where).order_by('-created_at')
        paginator = Paginator(items, page_size, request=request, pre_name=u"升级包")
        page = paginator.page(page_num)

        return render(request, 'node/upgrade/index.html', {
            'nav': 'node',
            'page': page,
            'keyword': keyword,
            'engines': get_all_engine(),
            'node_role': NODE_ROLE_TYPE,
            'version': get_current_client_version,
        })


@login_required
@ensure_csrf_cookie
def show(request, upgrade_id):
    """
    :param request:
    :param upgrade_id:
    :return:
    """
    model = UpgradePackageInfo.objects.filter(id=upgrade_id).first()

    return render(request, 'node/upgrade/changelog.html', {
            'nav': 'node',
            'model': model,
            'changelog': markdown.markdown(model.changelog),
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


@login_required
def download(request, upgrade_id):
    """
    :param request:
    :param upgrade_id:
    :return:
    """
    model = UpgradePackageInfo.objects.filter(id=upgrade_id).first()
    if model and model.path:
        file_name = os.path.basename(model.path)
        file = open(model.path, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/tar+gzip'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
        return response
    else:
        return Http404()


@login_required
def archive(request):
    """

    :param request:
    :return:
    """
    ids = request.POST.get('ids', '')
    try:
        UpgradePackageInfo.objects.filter(id__in=[i for i in ids.split(',') if i]).update(is_archive=True)
        return JsonResponse({"status": "ok"}, safe=False)
    except Exception as ex:
        import traceback;
        traceback.print_exc()
        return JsonResponse({"status": "failed", 'msg': str(ex)}, safe=False)
