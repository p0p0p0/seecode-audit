# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.cache import cache
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

from seecode.libs.dal.permission import get_permissions_by_all_module
from seecode.libs.units import parse_int, perm_verify
from seecode.libs.paginator import Paginator
from seecode.libs.dal.permission import get_permissions_by_all_module
from seecode.libs.dal.permission import delete_user_per_cache
from seecode.libs.dal.group import get_group_obj, is_association_settings
from seecode.libs.dal.permission import SYSTEM_CACHE


@login_required
@ensure_csrf_cookie
@perm_verify(['auth.view_group'])
def index(request):
    """
    :param request:
    :return:
    """
    if request.method == 'POST':
        save(request)
        return HttpResponseRedirect('/sys/group/')
    else:
        page_num = parse_int(request.GET.get('p', 1), 1)
        page_size = parse_int(request.GET.get('ps', 15), 15)
        modules = get_permissions_by_all_module()
        items = Group.objects.all()
        paginator = Paginator(items, page_size, request=request, pre_name=u"用户组")
        page = paginator.page(page_num)

        return render(request, 'system/account/group/index.html', {
            'nav': 'sys',
            'page': page,
            'modules': modules,
        })


@login_required
@ensure_csrf_cookie
@perm_verify(['auth.change_group', 'auth.add_group'])
def show(request, group_id):
    """
    :param request:
    :param group_id:
    :return:
    """
    if request.method == 'POST':
        name = request.POST.get('name', '')
        perms = request.POST.getlist('perms', '')
        group_obj = Group.objects.get(id=int(group_id))
        group_obj.name = name.strip()
        group_obj.save()
        perms_all = Permission.objects.all()
        for perm in perms_all:
            if str(perm.id) not in perms:
                group_obj.permissions.remove(perm)
            else:
                group_obj.permissions.add(perm)
        return HttpResponseRedirect('/sys/group/{0}/'.format(group_id))
    else:
        model = Group.objects.get(id=group_id)
        modules = get_permissions_by_all_module()

        return render(request, 'system/account/group/edit.html', {
            'nav': 'sys',
            'model': model,
            'modules': modules,
        })


@login_required
@perm_verify(['auth.change_group', 'auth.add_group'])
def save(request):
    """
    :param request:
    :return:
    """
    name = request.POST.get('name', '')
    perms = request.POST.getlist('perms', '')
    try:
        if name:
            try:
                Group.objects.get(name=name)
            except Group.DoesNotExist as ex:
                group = Group(name=name.strip())
                group.save()
                for perm_id in perms:
                    perm_obj = Permission.objects.get(id=int(perm_id))
                    group.permissions.add(perm_obj)
    except Exception as ex:
        raise ex

    return HttpResponseRedirect("/sys/group")


@login_required
@ensure_csrf_cookie
@perm_verify(['auth.view_group', 'auth.change_group'])
def member_index(request, group_id):
    """
    :param request:
    :param group_id:
    :return:
    """

    if request.method == 'POST':
        name = request.POST.get('name', '')
        print(name)
        user = User.objects.get_by_natural_key(name)
        group = get_group_obj(group_id=int(group_id))
        if group:
            user.groups.add(group)
            delete_user_per_cache(user_id=user.id)
            cache.set('permission_settings', None, 0)

        return HttpResponseRedirect("/sys/group/member/{0}".format(group_id))
    else:

        group = get_group_obj(group_id=group_id)
        page_num = parse_int(request.GET.get('p', 1), 1)
        page_size = parse_int(request.GET.get('ps', 15), 15)

        items = group.user_set.all()
        paginator = Paginator(items, page_size, request=request, pre_name=u"用户")
        page = paginator.page(page_num)

        return render(request, 'system/account/group/member.html', {
            'nav': 'sys',
            'page': page,
            'group': group,
        })


@login_required
@ensure_csrf_cookie
@perm_verify(['auth.delete_group'])
def member_batch(request):
    """
    :param request:
    :return:
    """

    action = request.POST.get('action', '')
    ids = request.POST.get('ids', '')
    group_id = request.POST.get('group_id', '')
    result = {'status': 'ok'}

    try:
        if action == 'remove':
            users = User.objects.filter(id__in=[i for i in ids.split(',') if i])
            group = get_group_obj(group_id=int(group_id))
            for item in users:
                item.groups.remove(group)
                delete_user_per_cache(user_id=item.id)

        if action == 'del':
            groups = Group.objects.filter(id__in=[i for i in ids.split(',') if i])

            for group in groups:
                if not is_association_settings(group.id) and group.id not in (3, 4):
                    for user in group.user_set.all():
                        user.groups.remove(group)
                    group.permissions.filter().delete()
                    group.delete()
                else:
                    result['status'] = 'no'
        cache.set('permission_settings', None, 0)
        cache_key = '{0}:{1}'.format(SYSTEM_CACHE[3], request.user.id)
        cache.set(cache_key, None, 0)
    except Exception as ex:
        pass

    return JsonResponse(result, safe=False)