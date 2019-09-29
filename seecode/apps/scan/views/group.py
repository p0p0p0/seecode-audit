# coding: utf-8
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.http import urlquote
from django.views.decorators.csrf import ensure_csrf_cookie

from seecode.apps.scan.models import ScanProfileInfo
from seecode.apps.scan.models import TaskGroupInfo
from seecode.libs.core.enum import TASK_GROUP_TYPE
from seecode.libs.dal.periodic import create_periodic_obj
from seecode.libs.dal.scan_group import create_t_group_obj
from seecode.libs.dal.scan_group import delete_t_by_list
from seecode.libs.dal.scan_group import get_all_group as get_all_task_group
from seecode.libs.dal.scan_group import get_t_group_by_id
from seecode.libs.dal.scan_group import get_t_group_by_name
from seecode.libs.dal.scan_group import update_t_group_obj
from seecode.libs.dal.scan_profile import get_profile_all
from seecode.libs.dal.scan_profile import get_profile_by_id
from seecode.libs.dal.sched import get_sched_all
from seecode.libs.dal.sched import get_sched_by_id
from seecode.libs.paginator import Paginator
from seecode.libs.units import parse_bool
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
            return HttpResponseRedirect('/scan/group/?msg={0}'.format(urlquote('创建任务成功!')))
        except Exception as ex:
            import traceback;
            traceback.print_exc()
            return HttpResponseRedirect('/scan/group/?errmsg={0}'.format(urlquote(str(ex))))
    else:
        keyword = request.GET.get('k', '')

        page_num = parse_int(request.GET.get('p', 1), 1)
        page_size = parse_int(request.GET.get('ps', 20), 20)

        sql_where = {}

        if keyword:
            sql_where['name__icontains'] = keyword.strip()

        items = TaskGroupInfo.objects.filter(**sql_where).order_by('-created_at')
        paginator = Paginator(items, page_size, request=request, pre_name=u"分组")
        page = paginator.page(page_num)

        return render(request, 'scan/group/index.html', {
            'nav': 'scan',
            'page': page,
            'keyword': keyword,
            'template_list': get_profile_all(),
            'sched_list': get_sched_all(),
            'group_type_list': TASK_GROUP_TYPE,
            'task_group_list': TASK_GROUP_TYPE,
        })


@login_required
@ensure_csrf_cookie
def show(request, group_id):
    """
    :param request:
    :param group_id:
    :return:
    """
    if request.method == 'POST':
        name = request.POST.get('name', '')
        profile = request.POST.get('profile', '')
        update_t_group_obj(
            group_id=group_id,
            name=name,
            profile_obj=get_profile_by_id(profile),
        )
        return HttpResponseRedirect("/scan/group/{0}/".format(group_id))
    else:
        model = get_t_group_by_id(group_id=group_id)
        scan_templates = ScanProfileInfo.objects.filter()

        return render(request, 'scan/group/edit.html', {
            'nav': 'scan',
            'model': model,
            'scan_templates': scan_templates,
        })


@login_required
def save(request):
    """
    :param request:
    :return:
    """
    name = request.POST.get('name', '')
    profile = request.POST.get('profile', '')
    scan_type = request.POST.get('scan_type', -1)

    grp = get_t_group_by_name(name=name)
    if grp:
        raise Exception('"{0}"分组已存在!'.format(name))
    if not all((profile, scan_type)):
        raise Exception('缺少"profile, scan_type" 参数!')
    project_list = []
    profile_id = int(profile)
    scan_type = int(scan_type)

    profile_obj = get_profile_by_id(profile_id=profile_id)
    if not profile_obj:
        raise Exception('"{0}"配置模板未找到!'.format(profile_id))

    periodic_obj = None
    project_list_ids = ['{0}'.format(p.id) for p in project_list]
    sched_obj = None
    if scan_type != -1:
        sched_obj = get_sched_by_id(sched_id=int(scan_type))
        periodic_obj = create_periodic_obj(
            name=name.strip(),
            interval=sched_obj.interval,
            crontab=sched_obj.crontab,
            args=','.join(project_list_ids),
        )

    create_t_group_obj(
        profile_obj=profile_obj,
        periodic_obj=periodic_obj,
        sched_obj=sched_obj,
        name=name,
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
        result_list = None

        if role == 'task_group':
            if keyword:
                result_list = TaskGroupInfo.objects.filter(name__icontains=keyword.strip())
            else:
                result_list = get_all_task_group()

        if result_list:
            for item in result_list:

                if role == 'task_group':
                    result.append({
                        "id": item.id,
                        "text": '{0}'.format(item.name)})
        return JsonResponse(result, safe=False)

    except Exception as ex:
        import traceback;
        traceback.print_exc()
        return JsonResponse({"status": "failed", 'msg': ex.__repr__()}, safe=False)


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
            delete_t_by_list(id_list)
        elif action == 'set-default':
            gid = request.POST.get('gid', '')
            update_t_group_obj(group_id=gid, is_default=True)
        return JsonResponse({"status": "ok"}, safe=False)
    except Exception as ex:
        return JsonResponse({"status": "failed", 'msg': ex.__repr__()}, safe=False)
