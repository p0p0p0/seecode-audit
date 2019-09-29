# coding: utf-8
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie

from seecode.apps.project.models.member import MemberInfo
from seecode.libs.paginator import Paginator
from seecode.libs.units import parse_int


@login_required
@ensure_csrf_cookie
def index(request):
    """
    :param request:
    :return:
    """
    state = request.GET.get('s', 'active')
    keyword = request.GET.get('k', '')

    page_num = parse_int(request.GET.get('p', 1), 1)
    page_size = parse_int(request.GET.get('ps', 20), 20)

    sql_where = {}

    if state:
        sql_where['state'] = state

    if keyword:
        keyword = keyword.strip()
        sql_where['username__icontains'] = keyword

    items = MemberInfo.objects.filter(**sql_where).order_by('-created_at')
    paginator = Paginator(items, page_size, request=request, pre_name=u"成员")
    page = paginator.page(page_num)

    return render(request, 'project/member/index.html', {
        'nav': 'pro',
        'page': page,
        'keyword': keyword,
        's': state,
    })


@login_required
@ensure_csrf_cookie
def show(request, intel_id):
    """
    :param request:
    :param intel_id:
    :return:
    """
    model = get_intelligence_obj(intel_id=intel_id)

    return render(request, 'project/member/edit.html', {
        'nav': 'monitor',
        'model': model,
    })


@login_required
@ensure_csrf_cookie
def save(request):
    """
    :param request:
    :return:
    """
    intel_id = request.POST.get('intel_id', '')
    title = request.POST.get('title', '')
    alarm_enable = request.POST.get('alarm_enable', False)
    api_url = request.POST.get('api_url', '')
    patch_adapter = request.POST.get('patch_adapter', '')
    alarm_template = request.POST.get('alarm_template', '')

    try:
        if title and intel_id:
            intel_obj = SafetyIntelligence.objects.get(id=int(intel_id))

            intel_obj.title = title.strip()
            if alarm_enable:
                intel_obj.patch_alarm_status = 2
                intel_obj.patch_api_url = api_url.strip()
                intel_obj.patch_adapter = patch_adapter.strip()
                intel_obj.patch_alarm_template = alarm_template.strip()

            intel_obj.save()
    except Exception as ex:
        import traceback;
        traceback.print_exc()
        raise ex

    return HttpResponseRedirect("/monitor/cve")
