# coding: utf-8
from __future__ import unicode_literals

import pinyin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.http import urlquote
from django.views.decorators.csrf import ensure_csrf_cookie

from seecode.apps.project.models.group import GroupInfo
from seecode.apps.project.models.item import ProjectInfo
from seecode.libs.core.enum import APP_TYPE
from seecode.libs.core.enum import LOG_LEVEL
from seecode.libs.dal.config import get_config
from seecode.libs.dal.gitlab_group import create_group_obj
from seecode.libs.dal.gitlab_group import get_group_by_id
from seecode.libs.dal.gitlab_group import get_group_by_name
from seecode.libs.dal.gitlab_group import get_group_top20
from seecode.libs.dal.gitlab_project import get_project_top50
from seecode.libs.dal.syslog import create_syslog_obj
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
            name = request.POST.get('name')
            if not name:
                raise Exception('分组名称不能为空！')
            if get_group_by_name(name=name.strip()):
                raise Exception('分组已存在！')

            group_type = parse_int(request.POST.get('type'), 1)

            key = pinyin.get(name, format='strip', delimiter="")
            create_group_obj(
                name=name,
                description=request.POST.get('description'),
                web_url=request.POST.get('url'),
                path=key,
                full_path=key,
                type=group_type,
                user=request.user
            )
            return HttpResponseRedirect('/project/group/?msg={0}'.format(urlquote('创建分组成功!')))
        except Exception as ex:
            return HttpResponseRedirect('/project/group/?errmsg={0}'.format(urlquote(str(ex))))
    else:
        keyword = request.GET.get('k', '')
        at = request.GET.get('a', '')
        page_num = parse_int(request.GET.get('p', 1), 1)
        page_size = parse_int(request.GET.get('ps', 20), 20)

        sql_where = {}

        if keyword:
            sql_where['name__icontains'] = keyword.strip()
        if at:
            sql_where['type'] = int(at)

        items = GroupInfo.objects.filter(**sql_where).order_by('-created_at')
        paginator = Paginator(items, page_size, request=request, pre_name=u"项目组")
        page = paginator.page(page_num)

        return render(request, 'project/group/index.html', {
            'nav': 'pro',
            'page': page,
            'app_type': APP_TYPE,
            'keyword': keyword,
            'at': at,
        })


@login_required
@ensure_csrf_cookie
def show(request, group_id):
    """
    :param request:
    :param group_id:
    :return:
    """

    model = get_group_by_id(group_id=group_id)
    if not model:
        return HttpResponseRedirect('/project/group/?errmsg={0}'.format(urlquote('分组未找到!')))

    conf = get_config()
    if conf and model:
        api_url = '{0}groups/{1}'.format(conf['gitlab']['api_url'], model.git_id)
    return render(request, 'project/group/edit.html', {
        'nav': 'pro',
        'model': model,
        'api_url': api_url,
    })


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
            group_list = GroupInfo.objects.filter(id__in=[i for i in ids.split(',') if i])
            for group in group_list:
                obj = ProjectInfo.objects.filter(group__id=group.id).first()
                if obj:
                    raise Exception("'{0}' 分类下存在项目, 请删除项目后在删除该分组。".format(group.name))
                group.delete()
        return JsonResponse({"status": "ok"}, safe=False)
    except Exception as ex:
        import traceback;
        traceback.print_exc()
        create_syslog_obj(
            title='删除项目分组失败',
            description=str(ex),
            stack_trace=traceback.format_exc(),
            level=LOG_LEVEL.ERROR
        )
        return JsonResponse({"status": "failed", 'msg': str(ex)}, safe=False)


@login_required
@ensure_csrf_cookie
def search(request):
    """
    :param request:
    :return:
    """
    keyword = request.POST.get('q', '')
    group_id = request.POST.get('group_id', '')
    role = request.POST.get('role', '')

    try:
        result = []
        result_list = None

        if role == 'group':
            if keyword:
                result_list = GroupInfo.objects.filter(name__icontains=keyword.strip())
            else:
                result_list = get_group_top20()

        elif role == 'project':
            sql_where = {}

            if group_id:
                sql_where['group__id'] = int(group_id)
            if keyword:
                sql_where['name__icontains'] = keyword.strip()

            if sql_where:
                result_list = ProjectInfo.objects.filter(**sql_where)
            else:
                result_list = get_project_top50()

        if result_list:
            for item in result_list:
                if role == 'group':
                    result.append({
                        "id": item.id,
                        "text": '{0}'.format(item.name)})
                elif role == 'project':
                    result.append({
                        "id": item.id,
                        "text": '{0}'.format(item.name)})

        return JsonResponse(result, safe=False)

    except Exception as ex:
        import traceback;
        traceback.print_exc()
        return JsonResponse({"status": "failed", 'msg': str(ex)}, safe=False)


@login_required
@ensure_csrf_cookie
def exists(request):
    """
    :param request:
    :return:
    """
    keyword = request.POST.get('q', '')

    try:
        if keyword:
            result_list = GroupInfo.objects.filter(name=keyword.strip()).first()
            if result_list:
                return JsonResponse({"status": 1, 'msg': "您输入的 \"{0}\" 分组名已存在，请从新输入。".format(keyword.strip())}, safe=False)
            else:
                return JsonResponse({"status": 0, 'msg': "当前分组不存在。"}, safe=False)

    except Exception as ex:
        import traceback;
        traceback.print_exc()
        return JsonResponse({"status": "failed", 'msg': str(ex)}, safe=False)
