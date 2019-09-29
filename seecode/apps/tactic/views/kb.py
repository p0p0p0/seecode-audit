# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import time

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.utils.http import urlquote
from django.views.decorators.csrf import ensure_csrf_cookie

from seecode.apps.tactic.models import VulnCategoryInfo
from seecode.apps.tactic.models import VulnInfo
from seecode.libs.core.common import make_dir
from seecode.libs.core.enum import RISK_TYPE
from seecode.libs.dal.tag import get_tag_obj_by_id
from seecode.libs.dal.tag import bulk_tag
from seecode.libs.dal.vuln import create_vuln_obj
from seecode.libs.dal.vuln import get_vuln_by_id
from seecode.libs.dal.vuln import update_vuln_obj
from seecode.libs.dal.vuln_cate import get_cate_obj_by_id
from seecode.libs.dal.vuln_cate import get_origin_all_list
from seecode.libs.paginator import Paginator
from seecode.libs.units import handle_uploaded_file
from seecode.libs.units import parse_int


@login_required
@ensure_csrf_cookie
def index(request):
    """
    :param request:
    :return:
    """
    if request.method == 'POST':
        try:
            show(request)
            return HttpResponseRedirect('/tactic/kb/?msg={0}'.format(urlquote('添加漏洞成功!')))
        except Exception as ex:
            return HttpResponseRedirect('/tactic/kb/?errmsg={0}'.format(urlquote(str(ex))))
    else:
        cate = request.GET.get('c', '')
        keyword = request.GET.get('k', '')

        page_num = parse_int(request.GET.get('p', 1), 1)
        page_size = parse_int(request.GET.get('ps', 20), 20)
        cate_list = VulnCategoryInfo.objects.filter(parent__isnull=True)
        origin_list = get_origin_all_list()
        sql_where = {}

        if cate:
            sql_where['origin__id'] = int(cate)

        items = VulnInfo.objects.filter(**sql_where).order_by("-created_at")
        paginator = Paginator(items, page_size, request=request, pre_name=u"漏洞")
        page = paginator.page(page_num)

        return render(request, 'tactic/kb/index.html', {
            'nav': 'tactic',
            'page': page,
            'keyword': keyword,
            'cate_list': cate_list,
            'origin_list': origin_list,
            'risk_list': RISK_TYPE,
        })


@login_required
@ensure_csrf_cookie
def show(request, vuln_id=None):
    """
    :param request:
    :param vuln_id:
    :return:
    """
    if request.method == 'POST':
        title = request.POST.get('title', '')
        cate = request.POST.get('cate', '')
        origin = request.POST.get('origin', '')
        risk = request.POST.get('risk', '')
        find_time = request.POST.get('find_time', '')
        cve = request.POST.get('cve', '')
        cnnvd = request.POST.get('cnnvd', '')
        cnvd = request.POST.get('cnvd', '')
        impact_version = request.POST.get('impact_version', '')
        tags = request.POST.get('tags', '')
        intro = request.POST.get('intro', '')
        solution = request.POST.get('solution', '')
        cate_obj = get_cate_obj_by_id(cate_id=int(cate))
        origin_obj = get_tag_obj_by_id(tag_id=int(origin))

        if vuln_id:
            vuln_obj = update_vuln_obj(
                vuln_id=vuln_id,
                cate_obj=cate_obj,
                origin=origin_obj,
                title=title,
                description=intro,
                solution=solution,
                reference='',
                risk=risk,
                impact_version=impact_version,
                cnnvd=cnnvd,
                cnvd=cnvd,
                cve=cve,
                find_time=find_time,
            )
        else:
            vuln_obj = save(request)

        if vuln_obj:
            vuln_obj.tags.clear()
            tags = bulk_tag(tags, 3)
            vuln_obj.tags.add(*tags)

        return HttpResponseRedirect('/tactic/kb/{0}/'.format(vuln_id))
    else:
        cate_list = VulnCategoryInfo.objects.filter(parent__isnull=True)
        origin_list = get_origin_all_list()
        model = ''
        tags = []
        if vuln_id:
            model = get_vuln_by_id(vuln_id=vuln_id)
            tags = [_.name for _ in model.tags.all()]
            tags = ','.join(tags)

        return render(request, 'tactic/kb/edit.html', {
            'nav': 'tactic',
            'model': model,
            'cate_list': cate_list,
            'origin_list': origin_list,
            'risk_list': RISK_TYPE,
            'tags': tags,
        })


@login_required
def save(request):
    """
    :param request:
    :return:
    """
    title = request.POST.get('title', '')
    cate = request.POST.get('cate', '')
    origin = request.POST.get('origin', '')
    risk = request.POST.get('risk', 5)
    find_date = request.POST.get('find_date', '')
    cve = request.POST.get('cve', '')
    cnnvd = request.POST.get('cnnvd', '')
    cnvd = request.POST.get('cnvd', '')
    impact_version = request.POST.get('impact_version', '')
    intro = request.POST.get('intro', '')
    solution = request.POST.get('solution', '')

    if not title:
        raise Exception('漏洞标题必须输入!')

    if title and len(title) > 255:
        title = title[:255]

    risk = int(risk)
    cate_obj = get_cate_obj_by_id(cate_id=int(cate))
    origin_obj = get_tag_obj_by_id(tag_id=int(origin))

    vuln_obj = create_vuln_obj(
            cate_obj=cate_obj,
            origin=origin_obj,
            title=title,
            description=intro,
            solution=solution,
            reference='',
            risk=risk,
            impact_version=impact_version,
            cnnvd=cnnvd,
            cnvd=cnvd,
            cve=cve,
            find_time=find_date,
        )
    return vuln_obj


@login_required
@ensure_csrf_cookie
def upload(request):
    """
    :param request:
    :return:
    """
    file_url = ''
    file_name = ''
    try:
        file_obj = request.FILES.get('file')
        _, ext = os.path.splitext(file_obj.name)
        file_name = '{0}{1}'.format(str(int(time.time())), ext)
        data_path = os.path.join(settings.UPLOAD_ROOT, 'kb')
        make_dir(data_path)
        upload_file = os.path.join(data_path, file_name)

        handle_uploaded_file(request.FILES['file'], upload_file)
        file_url = 'http://{0}{1}kb/{2}'.format(request.META['HTTP_HOST'], settings.UPLOAD_URL, file_name)
    except Exception as ex:
        import traceback;traceback.print_exc()

    return JsonResponse({
        "url_img": file_url,
        "img": '/upload/kb/{0}'.format(file_name),
        "name": file_name,
    }, safe=True)


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
            VulnInfo.objects.filter(id__in=[i for i in ids.split(',') if i]).delete()
        return JsonResponse({"status": "ok"}, safe=False)
    except Exception as ex:
        import traceback;
        traceback.print_exc()
        return JsonResponse({"status": "failed", 'msg': ex.__repr__()}, safe=False)


@login_required
@ensure_csrf_cookie
def search(request):
    """
       :param request:
       :return:
       """
    keyword = request.POST.get('q', '')

    try:
        result = []
        if keyword:
            result_list = VulnInfo.objects.filter(title__icontains=keyword.strip())
            for item in result_list:
                result.append({
                    "id": item.id,
                    "name": '{0}'.format(item.title)})
        return JsonResponse(result, safe=False)

    except Exception as ex:
        import traceback;
        traceback.print_exc()
        return JsonResponse({"status": "failed", 'msg': ex.__repr__()}, safe=False)
