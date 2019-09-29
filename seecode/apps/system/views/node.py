# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import time
"""
https://stackoverflow.com/questions/9105649/how-to-use-pysnmp-to-monitor-system-resources
"""

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.db.models import Count
from django.db.models import Max,Avg,F,Q

from seecode.libs.paginator import Paginator
from seecode.libs.units import parse_int, handle_uploaded_file, perm_verify


@login_required
@ensure_csrf_cookie
@perm_verify(['system.view_employeeinfo'])
def index(request):
    """
    :param request:
    :return:
    """

    name = request.GET.get('n', '')
    level = request.GET.get('l', '')
    grade = request.GET.get('g', '')
    status = request.GET.get('s', '1')

    page_num = parse_int(request.GET.get('p', 1), 1)
    page_size = parse_int(request.GET.get('ps', 20), 20)



    sql_where = {}

    if name:
        sql_where['name__icontains'] = name

    if level:
        sql_where['department__level'] = int(level)

    if status:
        sql_where['status'] = int(status)

    if grade:
        if grade == '-':
            sql_where['grade_level'] = ""
        else:
            sql_where['grade_level'] = grade

    items = '' #EmployeeInfo.objects.filter(**sql_where).order_by('-modified_on')
    paginator = Paginator(items, page_size, request=request, pre_name=u"员工")
    page = paginator.page(page_num)

    return render(request, 'system/node/index.html', {
        'nav': 'sys',
        'page': page,
        'level': level,
        'name': name,
        'status': status,
        'grade': grade,

    })


@login_required
@ensure_csrf_cookie
@perm_verify(['system.view_employeeinfo'])
def show(request, employee_id):
    """
    :param request:
    :param employee_id:
    :return:
    """

    if request.user.is_superuser:

        model = get_employee_obj(employee_id=employee_id)

        return render(request, 'system/employee/show.html', {
            'nav': 'sys',
            'model': model,
        })
    else:
        return HttpResponseRedirect("/sys/employee")


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

    employees = EmployeeInfo.objects.filter(account_name__icontains=user_name)

    result = []
    for item in employees:
        result.append({
            "id": item.id,
            "name": '{0}({1})'.format(item.name, item.email)})
    return JsonResponse(result, safe=False)


@login_required
@ensure_csrf_cookie
@perm_verify(['system.add_employeeinfo'])
def data_import(request):
    """
    :param request:
    :return:
    """
    if request.method == 'POST':
        dept_path = '{0}/employee_{1}.json'.format(settings.UPLOAD_DIR, str(int(time.time())))
        handle_uploaded_file(request.FILES['file'], dept_path)
        with open(dept_path) as fp:
            json_obj = json.load(fp)

            if json_obj['Data']:
                for item in json_obj['Data']:
                    sync_employee(item)
    return HttpResponseRedirect('/sys/employee')


@login_required
@ensure_csrf_cookie
@perm_verify(['system.change_employeeinfo'])
def batch(request):
    """
    :param request:
    :return:
    """
    user_code = request.POST.get('user_code', '')
    action = request.POST.get('action', '')

    if action and 'leader' == action and user_code:
        oa = OA()
        is_success, leader = oa.get_direct_leader(user_code)

        if is_success:
            employee = get_employee_obj(hr_code=user_code)
            if employee:
                employee.direct_leader_hrcode = leader['user_code']
                employee.save()
        else:
            pass
            #TODO 记录到syslog中

    return JsonResponse({"status": "ok"}, safe=False)
