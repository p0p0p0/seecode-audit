# coding: utf-8
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.http import urlquote
from django.views.decorators.csrf import ensure_csrf_cookie

from seecode.apps.project.models.app import ApplicationInfo
from seecode.apps.project.models.app import FileStatisticsInfo
from seecode.apps.project.models.item import RepositoryInfo
from seecode.libs.core.exceptions import ParameterIsEmptyException
from seecode.libs.dal.application import create_app_obj
from seecode.libs.dal.application import delete_app_list
from seecode.libs.dal.application import get_app_by_app_name
from seecode.libs.dal.application import get_app_by_id
from seecode.libs.dal.application import get_app_by_module_name
from seecode.libs.dal.application import get_app_risk_by_id
from seecode.libs.dal.gitlab_group import get_group_by_id
from seecode.libs.dal.gitlab_project import get_project_by_id
from seecode.libs.dal.gitlab_repository import get_repository_by_id
from seecode.libs.paginator import Paginator
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
            save(request)
            name = request.POST.get('name', None)
            return HttpResponseRedirect('/project/app/?msg={0}'.format(urlquote('创建"{0}"应用成功!'.format(name))))
        except Exception as ex:
            import traceback;traceback.print_exc()
            return HttpResponseRedirect('/project/app/?errmsg={0}'.format(urlquote(str(ex))))
    else:
        group_id = request.GET.get('g', '')
        project_id = request.GET.get('pro', '')
        risk = request.GET.get('r', '')
        archive = request.GET.get('archive', '')
        form_dt = request.GET.get('dt', '')
        group_obj = None
        project_obj = None

        page_num = parse_int(request.GET.get('p', 1), 1)
        page_size = parse_int(request.GET.get('ps', 20), 20)

        sql_where = {
            'is_archive': False
        }
        if archive == '1':
            sql_where['is_archive'] = True
        if group_id:
            group_obj = get_group_by_id(group_id=group_id)
            sql_where['project__group__id'] = int(group_id)

        if project_id:
            project_obj = get_project_by_id(project_id=project_id)
            sql_where['project__id'] = int(project_id)
        if risk:
            if risk == '1':
                sql_where['risk_scope__gt'] = 300
            elif risk == '2':
                sql_where['risk_scope__gt'] = 200
                sql_where['risk_scope__lte'] = 300
            elif risk == '3':
                sql_where['risk_scope__lte'] = 200
            elif risk == '4':
                sql_where['status'] = 1
            elif risk == '5':
                sql_where['status__in'] = [2, 3]
        if form_dt:
            try:
                start_date, end_date = form_dt.split(" - ")
                sql_where['last_scan_time__gte'] = '{0} 00:00:00'.format(start_date)
                sql_where['last_scan_time__lte'] = '{0} 23:59:59'.format(end_date)
            except:
                pass

        items = ApplicationInfo.objects.filter(**sql_where).order_by('-last_scan_time')
        paginator = Paginator(items, page_size, request=request, pre_name=u"应用")
        page = paginator.page(page_num)

        return render(request, 'project/app/index.html', {
            'nav': 'pro',
            'page': page,
            'form_dt': form_dt,
            'group_obj': group_obj,
            'project_obj': project_obj,
            'archive': archive,
            'r': risk,
        })


@login_required
@ensure_csrf_cookie
def show(request, app_id):
    """
    :param request:
    :param app_id:
    :return:
    """

    model = get_app_by_id(app_id=app_id)

    if not model:
        return HttpResponseRedirect('/project/app/?errmsg={0}'.format(u'项目未找到!'))

    file_list = FileStatisticsInfo.objects.filter(app__id=app_id)
    risk_statistics = get_app_risk_by_id(app_id=app_id)

    return render(request, 'project/app/show.html', {
        'nav': 'pro',
        'model': model,
        'file_list': file_list,
        'risk_statistics': risk_statistics,
    })


@login_required
def save(request):
    """
    :param request:
    :return:
    """
    result = False
    name = request.POST.get('name', None)
    module_name = request.POST.get('module_name', '')
    group_id = request.POST.get('group', None)
    project_id = request.POST.get('project', None)
    branch_id = request.POST.get('branch', None)

    if not all((name, project_id, branch_id)):
        raise ParameterIsEmptyException('"name, project_id, branch_id" parameter cannot be empty.')

    app_obj = get_app_by_app_name(name=name, project_id=project_id)
    if app_obj:
        raise Exception('"{0}" 应用已存在!'.format(name))

    app_obj = get_app_by_module_name(name=name, project_id=project_id)
    if app_obj:
        raise Exception('"{0}" 应用模块名称已存在!'.format(module_name))

    project_obj = get_project_by_id(project_id=project_id)
    repo_obj = get_repository_by_id(repo_id=branch_id)

    app = create_app_obj(
        project_obj=project_obj,
        module_name=module_name,
        app_name=name,
        repo_obj=repo_obj,
    )
    if app:
        result = True
    return result


@login_required
@ensure_csrf_cookie
def search(request):
    """
    :param request:
    :return:
    """
    keyword = request.POST.get('q', '')
    project_id = request.POST.get('project_id', '')
    role = request.POST.get('role', '')

    try:
        result, result_list = [], []

        if role == 'branch':
            sql_where = {}
            if project_id:
                sql_where['project__id'] = int(project_id)
            if keyword:
                sql_where['name__icontains'] = keyword.strip()
            if sql_where:
                result_list = RepositoryInfo.objects.filter(**sql_where)
        elif role == 'app':
            sql_where = {}
            if project_id:
                sql_where['project__id'] = int(project_id)
            if keyword:
                sql_where['app_name__icontains'] = keyword.strip()

            result_list = ApplicationInfo.objects.filter(**sql_where)[:15]

        for item in result_list:
            if role == 'branch':
                result.append({
                    "id": item.id,
                    "text": '{0} ({1})'.format(item.name, item.last_short_id or '-')})
            elif role == 'app':
                result.append({
                    "id": item.id,
                    "text": '{0}'.format(item.module_name)})

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
    ids = request.POST.get('ids', '')
    action = request.POST.get('action', '')
    try:
        if action and 'del' == action:
            delete_app_list(id_list=[_ for _ in ids.split(',') if _])
        return JsonResponse({'status': 'ok'}, safe=False)
    except Exception as ex:
        return JsonResponse({'status': 'failed', 'msg': str(ex)}, safe=False)
