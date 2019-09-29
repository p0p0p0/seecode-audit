# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.authtoken.models import Token

from seecode.libs.paginator import Paginator
from seecode.libs.units import parse_bool
from seecode.libs.units import parse_int
from seecode.libs.units import perm_verify


@login_required
@ensure_csrf_cookie
@perm_verify(['auth.view_user', ])
def index(request):
    """
    :param request:
    :return:
    """
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        is_active = parse_bool(request.POST.get('active', ''))
        if not all((name, email, password1, password2)):
            raise Exception("缺少关键字。")
        if password1.strip() == password2.strip():
            user_obj = User(
                username=name.strip(),
                passord=password1.strip(),
                email=email.strip(),
                is_active=is_active,
            )
            user_obj.save()
        return HttpResponseRedirect("/sys/account/")

    else:
        status = request.GET.get('s', '')
        user_name = request.GET.get('u', '')
        group_id = request.GET.get('g', '')

        page_num = parse_int(request.GET.get('p', 1), 1)
        page_size = parse_int(request.GET.get('ps', 15), 15)

        groups = Group.objects.all().order_by('-id')

        sql_where = {}

        if status:
            sql_where['is_active'] = True if int(status) == 1 else False
        if user_name:
            sql_where['username__icontains'] = user_name

        if group_id:
            group_obj = Group.objects.get(id=int(group_id))
            paginator = Paginator(group_obj.user_set.filter(**sql_where), page_size, request=request, pre_name=u"账户")
            page = paginator.page(page_num)
        else:
            items = User.objects.filter(**sql_where)
            paginator = Paginator(items, page_size, request=request, pre_name=u"账户")
            page = paginator.page(page_num)

        return render(request, 'system/account/index.html', {
            'nav': 'sys',
            'page': page,
            'status': status,
            'user_name': user_name,
            'groups': groups,
            'group': group_id,
        })


@login_required
@ensure_csrf_cookie
@perm_verify(['auth.add_user', 'auth.change_user'])
def show(request, user_id):
    """
    :param request:
    :param user_id:
    :return:
    """
    if request.method == 'POST':
        email = request.POST.get('email', '')
        status = request.POST.get('status', '')
        group_id = request.POST.get('group-id', '')

        if request.user.id == user_id:
            user = User.objects.get(id=user_id)
            if group_id:
                group_obj = Group.objects.get(id=int(group_id))
                for group in Group.objects.all():
                    if group.id != group_obj.id:
                        user.groups.remove(group)
                    else:
                        user.groups.add(group)
            if status:
                status = int(status)
                if status == 1:
                    user.is_active = True
                else:
                    user.is_active = False

            if email:
                user.email = email.strip()

            user.save()
        return HttpResponseRedirect("/sys/account/{0}/".format(user_id))
    else:
        model = User.objects.get(id=user_id)
        modules = ContentType.objects.all()
        groups = Group.objects.all()
        token = Token.objects.filter(user__id=model.id).first()

        return render(request, 'system/account/profile.html', {
            'nav': 'sys',
            'model': model,
            'modules': modules,
            'groups': groups,
            'token': token,
        })


@login_required
@ensure_csrf_cookie
@perm_verify(['auth.add_user', 'auth.change_user'])
def save(request):
    """
    :param request:
    :return:
    """
    email = request.POST.get('email', '')
    status = request.POST.get('status', '')
    group_id = request.POST.get('group-id', '')
    user_id = request.POST.get('user-id', '')

    try:

        if user_id and request.user.id != int(user_id):
            user = User.objects.get(id=int(user_id))
            if group_id:
                group_obj = Group.objects.get(id=int(group_id))
                for group in Group.objects.all():
                    if group.id != group_obj.id:
                        user.groups.remove(group)
                    else:
                        user.groups.add(group)
            if status:
                status = int(status)
                if status == 1:
                    user.is_active = True
                else:
                    user.is_active = False

            if email:
                user.email = email.strip()

            user.save()

    except Exception as ex:
        import traceback;
        traceback.print_exc()
        raise ex

    return HttpResponseRedirect("/sys/account/{0}".format(user_id))


@ensure_csrf_cookie
@perm_verify(['auth.add_user', 'auth.change_user'])
def token(request):
    """
    :param request:
    :return:
    """
    action = request.POST.get('action', '')
    ids = request.POST.get('ids', '')
    user_id = request.POST.get('user_id', '')
    result = {'status': 'ok'}

    try:
        if action == 'disable':
            User.objects.filter(id__in=[i for i in ids.split(',') if i]).update(is_active=False)
        elif action in ('token', 're-token'):
            try:
                user = User.objects.filter(id=user_id).first()
                token = Token.objects.get(user_id=user.id)
                if 're-token' == action:
                    Token.objects.get(user_id=user.id).delete()
                    token = Token.objects.create(user=user)
            except Token.DoesNotExist:
                token = Token.objects.create(user=user)

    except Exception as ex:
        import traceback;
        traceback.print_exc()

    return JsonResponse(result, safe=False)


@login_required
@ensure_csrf_cookie
@perm_verify(['system.view_employeeinfo'])
def search(request):
    """
    :param request:
    :return:
    """

    user_name = request.POST.get('q', '')
    if user_name:
        user_name = user_name.strip().lower()

    employees = User.objects.filter(username=user_name, is_active=True)

    result = []
    for item in employees:
        result.append({
            "id": item.id,
            "name": '{0}'.format(item.username)})
    return JsonResponse(result, safe=False)

