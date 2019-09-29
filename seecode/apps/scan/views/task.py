# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import ast
import codecs
import os

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.http import urlquote
from django.views.decorators.csrf import ensure_csrf_cookie

from seecode.apps.project.models.group import GroupInfo
from seecode.apps.project.models.item import ProjectInfo
from seecode.apps.scan.models import TaskGroupInfo
from seecode.apps.scan.models import TaskHistory
from seecode.apps.scan.models import TaskInfo
from seecode.libs.core.common import del_file
from seecode.libs.core.common import make_dir
from seecode.libs.core.data import conf
from seecode.libs.core.dispatchctl import dispatch_task
from seecode.libs.core.enum import LOG_LEVEL
from seecode.libs.core.enum import SCAN_STATUS
from seecode.libs.core.enum import TASK_GROUP_TYPE
from seecode.libs.dal.config import get_config
from seecode.libs.dal.scan_profile import get_profile_all
from seecode.libs.dal.scan_task import delete_by_list
from seecode.libs.dal.scan_task import get_task_by_id
from seecode.libs.dal.sched import get_sched_all
from seecode.libs.dal.syslog import create_syslog_obj
from seecode.libs.dal.application import get_app_by_id
from seecode.libs.paginator import Paginator
from seecode.libs.units import parse_bool
from seecode.libs.units import parse_int
from seecode.libs.utils.ftpwrapper import FTPWork
from seecode_scanner.tasks.scan import start as seecode_scanner_start


@login_required
@ensure_csrf_cookie
def index(request):
    """
    :param request:
    :return:
    """
    if request.method == 'POST':
        try:
            save(request)
            return HttpResponseRedirect('/scan/task/?msg={0}'.format(urlquote('下发扫描任务成功!')))
        except Exception as ex:
            import traceback;
            traceback.print_exc()
            return HttpResponseRedirect('/scan/task/?errmsg={0}'.format(urlquote(str(ex))))
    else:
        group = request.GET.get('g', '')
        status = request.GET.get('s', '')
        app = request.GET.get('a', '')
        keyword = request.GET.get('k', '')
        form_dt = request.GET.get('dt', '')

        page_num = parse_int(request.GET.get('p', 1), 1)
        page_size = parse_int(request.GET.get('ps', 20), 20)

        sql_where = {}

        if status:
            sql_where['status'] = int(status)
        if app:
            sql_where['app__id'] = int(app)
            app = get_app_by_id(app)
        if group:
            group = TaskGroupInfo.objects.filter(id=group).first()
        if form_dt:
            try:
                start_date, end_date = form_dt.split(" - ")
                sql_where['start_time__gte'] = '{0} 00:00:00'.format(start_date)
                sql_where['start_time__lte'] = '{0} 23:59:59'.format(end_date)
            except:
                pass

        items = TaskInfo.objects.filter(**sql_where).order_by('-created_at')
        paginator = Paginator(items, page_size, request=request, pre_name=u"任务")
        page = paginator.page(page_num)

        return render(request, 'scan/task/index.html', {
            'nav': 'scan',
            'page': page,
            's': status,
            'group': group,
            'app': app,
            'keyword': keyword,
            'form_dt': form_dt,
            'scan_status': SCAN_STATUS,
            'template_list': get_profile_all(),
            'sched_list': get_sched_all(),
            'group_type_list': TASK_GROUP_TYPE,
        })


@login_required
@ensure_csrf_cookie
def show(request, task_id):
    """
    :param request:
    :param task_id:
    :return:
    """
    model = get_task_by_id(task_id=task_id)
    config, history, time_consumed = {}, [], None
    if model.config:
        config = ast.literal_eval(model.config)
        history = TaskHistory.objects.filter(task__id=model.id)
        if model.end_time and model.start_time:
            time_consumed = model.end_time - model.start_time
            if settings.TIME_ZONE == 'Asia/Shanghai':
                times = str(time_consumed).split(':')
                time_consumed = times[0] + '时' + times[1] + '分' + str(round(float(times[2]), 2)) + '秒'

    return render(request, 'scan/task/show.html', {
        'nav': 'scan',
        'model': model,
        'config': config,
        'history': history,
        'time_consumed': time_consumed,
    })


@login_required
def save(request):
    """
    :param request:
    :return:
    """

    task_group_id = request.POST.get('task_group', '')
    task_type = request.POST.get('task_type', '')
    group_id = request.POST.get('group_id', '')
    app_id = request.POST.get('app_id', '')
    branch = request.POST.get('branch', '')
    is_force_scan = request.POST.get('is_force_scan', False)

    if not all((task_group_id, task_type)):
        raise Exception('缺少"task_group_id, task_type" 参数!')

    if group_id:
        group_id = int(group_id)
    if app_id:
        app_id = int(app_id)

    dispatch_task(
        task_group_id=int(task_group_id),
        task_type=int(task_type),
        group_id=group_id,
        app_id=app_id,
        branch=branch,
        is_force_scan=parse_bool(is_force_scan),
    )


@login_required
@ensure_csrf_cookie
def search(request):
    """
    :param request:
    :return:
    """
    keyword = request.POST.get('q', '')
    role = request.POST.get('role', '')

    try:
        result = []
        if keyword and role:
            if role == 'group':
                result_list = GroupInfo.objects.filter(name__icontains=keyword.strip())
            else:
                result_list = ProjectInfo.objects.filter(name__icontains=keyword.strip())

            for item in result_list:
                if role == 'group':
                    result.append({
                        "id": item.id,
                        "name": '{0} ({1})'.format(item.name, item.full_path)
                    })
                else:
                    result.append({
                        "id": item.id,
                        "name": '{0} ({1})'.format(item.name, item.path_with_namespace)
                    })
        return JsonResponse(result, safe=False)

    except Exception as ex:
        import traceback;
        traceback.print_exc()
        return JsonResponse({"status": "failed", 'msg': str(ex)}, safe=False)


@login_required
@ensure_csrf_cookie
def batch(request):
    """
    :param request:
    :return:
    """
    action = request.POST.get('action', '')
    ids = request.POST.get('ids', '')

    id_list = [i for i in ids.split(',') if i]

    try:
        if action == 'del':
            delete_by_list(id_list)
        elif action == 're-scan':
            task_list = TaskInfo.objects.filter(id__in=id_list, status__in=[1, 2])
            for task in task_list:
                kwargs = ast.literal_eval(task.config)
                seecode_scanner_start.delay(**kwargs)
        return JsonResponse({"status": "ok"}, safe=False)
    except Exception as ex:
        import traceback;
        traceback.print_exc()
        return JsonResponse({"status": "failed", 'msg': str(ex)}, safe=False)


def download_cloud_result(local_file, remote_file_log):
    """

    :param local_file:
    :param remote_file_log:
    :return:
    """
    try:
        web_conf = get_config()
        if web_conf['project']['upload_type'] == 2:
            if not conf.storage['ftp']:
                conf.storage['ftp'] = FTPWork(
                    host=web_conf['project']['ftp_host'],
                    port=web_conf['project']['ftp_port'],
                    username=web_conf['project']['ftp_username'],
                    password=web_conf['project']['ftp_password'],
                )
            conf.storage['ftp'].download_file(local_file, remote_file_log)
    except Exception as ex:
        import traceback
        create_syslog_obj(
            title='下载扫描日志失败',
            description=str(ex),
            stack_trace=traceback.format_exc(),
            level=LOG_LEVEL.ERROR
        )


@login_required
@ensure_csrf_cookie
def download_log(request, task_id):
    """

    :param request:
    :param task_id:
    :return:
    """
    task = TaskInfo.objects.filter(id=task_id).first()
    if task and task.log_file:
        local_log_dir = os.path.join(settings.MEDIA_ROOT, 'logs')
        make_dir(local_log_dir)
        remote_file_log = task.log_file
        local_file = os.path.join(local_log_dir, os.path.basename(task.log_file))
        del_file(local_file)
        download_cloud_result(local_file, remote_file_log)
        if os.path.isfile(local_file):
            with open(local_file, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="text/plain")
                response.write(codecs.BOM_UTF8)
                response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(local_file)
                return response
        else:
            return HttpResponseNotFound()
    else:
        return HttpResponseNotFound()
