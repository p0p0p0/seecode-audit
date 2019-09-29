# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie

from seecode.libs.paginator import Paginator
from seecode.libs.units import parse_int
from seecode.libs.units import perm_verify
from seecode.libs.units import strip


@login_required
@ensure_csrf_cookie
@perm_verify(['auth.view_permission'])
def index(request):
    """
    :param request:
    :return:
    """
    if request.method == 'POST':
        save(request)
        return HttpResponseRedirect("/sys/account/perm/")
    else:
        name = request.GET.get('n', '')
        module = request.GET.get('m', '')
        page_num = parse_int(request.GET.get('p', 1), 1)
        page_size = parse_int(request.GET.get('ps', 15), 15)
        modules = ContentType.objects.all()
        sql_where = {}

        if name:
            sql_where['name__icontains'] = name
        if module:
            sql_where['content_type__id'] = int(module)

        items = Permission.objects.filter(**sql_where).order_by('-id').order_by('-content_type__model')
        paginator = Paginator(items, page_size, request=request, pre_name=u"权限")
        page = paginator.page(page_num)

        return render(request, 'system/account/perm/index.html', {
            'nav': 'sys',
            'page': page,
            'modules': modules,
            'name': name,
            'module': module,
        })


@login_required
@ensure_csrf_cookie
@perm_verify(['auth.change_permission'])
def show(request, perm_id):
    """
    :param request:
    :param perm_id:
    :return:
    """
    if request.method == 'POST':
        name = strip(request.POST.get('name', ''))
        if name:
            perm = Permission.objects.get(id=int(perm_id))
            perm.name = name
            perm.save()
        return HttpResponseRedirect("/sys/account/perm/{0}/".format(perm_id))
    else:
        model = Permission.objects.get(id=perm_id)
        modules = ContentType.objects.all()

        return render(request, 'system/account/perm/edit.html', {
            'nav': 'sys',
            'model': model,
            'modules': modules,
        })


@login_required
@perm_verify(['auth.change_permission', 'auth.add_permission'])
def save(request):
    """
    :param request:
    :return:
    """
    name = request.POST.get('name', '')
    key = request.POST.get('key', '')
    module = request.POST.get('module', '')

    if module:
        content_type = ContentType.objects.get(id=int(module))
        perm = Permission(
            name=name,
            codename=key,
            content_type=content_type
        )
        perm.save()

    return HttpResponseRedirect("/sys/account/perm")


@login_required
@ensure_csrf_cookie
@perm_verify(['auth.delete_permission', ])
def delete(request):
    """
    :param request:
    :return:
    """
    ids = request.POST.get('ids', '')

    Permission.objects.filter(id__in=[_id for _id in ids.split(',') if _id]).delete()

    return JsonResponse({"status": "ok"}, safe=True)
