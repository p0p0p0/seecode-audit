# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie

from seecode.apps.system.models import TagInfo
from seecode.apps.tactic.models import VulnCategoryInfo
from seecode.libs.dal.tag import create_tag_obj
from seecode.libs.dal.tag import get_tag_obj_by_id
from seecode.libs.dal.tag import get_tag_obj_by_name
from seecode.libs.dal.tag import update_tag_obj
from seecode.libs.dal.vuln_cate import create_cate_obj
from seecode.libs.dal.vuln_cate import get_cate_obj_by_id
from seecode.libs.dal.vuln_cate import get_cate_obj_by_name
from seecode.libs.dal.vuln_cate import update_cate_obj
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
            action = request.POST.get('action')
            if  action == 'del':
                ids = request.POST.get('ids')
                #  TODO 检查待删除的分类是否有漏洞
                VulnCategoryInfo.objects.filter(id__in=[_ for _ in ids.split(',') if _]).delete()
                return HttpResponseRedirect('/tactic/kb/cate/')
            else:
                name = request.POST.get('name')
                key = request.POST.get('key')
                tag = request.POST.get('tag')
                parent = request.POST.get('parent')
                if not name:
                    raise Exception('分类名称不能为空！')
                if get_cate_obj_by_name(name=name.strip()):
                    raise Exception('分类已存在！')
                create_cate_obj(
                    name=name,
                    parent=parent,
                    key=key,
                    tag=tag,
                )
                return HttpResponseRedirect('/tactic/kb/cate/?msg={0}'.format(u'创建漏洞分类成功!'))
        except Exception as ex:
            return HttpResponseRedirect('/tactic/kb/cate/?errmsg={0}'.format(ex))
    else:
        keyword = request.GET.get('k', '')

        page_num = parse_int(request.GET.get('p', 1), 1)
        page_size = parse_int(request.GET.get('ps', 20), 20)

        sql_where = {
            'parent__isnull': True
        }

        if keyword:
            sql_where['name__icontains'] = keyword.strip()

        parent_list = VulnCategoryInfo.objects.filter(parent__isnull=True)
        items = VulnCategoryInfo.objects.filter(**sql_where).order_by('-created_at')
        paginator = Paginator(items, page_size, request=request, pre_name=u"漏洞分类")
        page = paginator.page(page_num)

        return render(request, 'tactic/kb/cate/index.html', {
            'nav': 'tactic',
            'page': page,
            'keyword': keyword,
            'parent_list': parent_list,
        })


@login_required
@ensure_csrf_cookie
def show(request, cate_id):
    """
    :param request:
    :param cate_id:
    :return:
    """
    model = get_cate_obj_by_id(cate_id=cate_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        key = request.POST.get('key')
        tag = request.POST.get('tag')
        parent = request.POST.get('parent')
        if not name:
            raise Exception('分类名称不能为空！')
        update_cate_obj(
            cate_id=cate_id,
            name=name,
            parent=parent,
            key=key,
            tag=tag,
        )
        return HttpResponseRedirect('/tactic/kb/cate/{0}/'.format(cate_id))
    else:
        parent_list = VulnCategoryInfo.objects.filter(parent__isnull=True)
        return render(request, 'tactic/kb/cate/edit.html', {
            'nav': 'tactic',
            'model': model,
            'parent_list': parent_list,
        })


@login_required
@ensure_csrf_cookie
def origin_index(request):
    """
    :param request:
    :return:
    """
    if request.method == 'POST':
        try:
            action = request.POST.get('action')
            if action == 'del':
                # TODO 检测来源是否有在使用
                ids = request.POST.get('ids')
                TagInfo.objects.filter(parent__id=1, id__in=[_ for _ in ids.split(',') if _]).delete()
                return  HttpResponseRedirect("/tactic/kb/origin/")
            if  action == 'update':
                id = request.POST.get('id')
                name = request.POST.get('name')
                update_tag_obj(
                    tag_id=id,
                    name=name
                )
                return  JsonResponse({"status": "ok"}, safe=True)
            else:
                name = request.POST.get('name')
                if not name:
                    raise Exception('来源名称不能为空！')
                if get_tag_obj_by_name(name=name.strip()):
                    raise Exception('来源已存在！')
                cate_obj = get_tag_obj_by_id(tag_id=1)
                create_tag_obj(name=name, parent=cate_obj)
                return HttpResponseRedirect('/tactic/kb/origin/?msg={0}'.format(u'创建漏洞来源成功!'))
        except Exception as ex:
            return HttpResponseRedirect('/tactic/kb/origin/?errmsg={0}'.format(ex))
    else:
        keyword = request.GET.get('k', '')

        page_num = parse_int(request.GET.get('p', 1), 1)
        page_size = parse_int(request.GET.get('ps', 20), 20)

        sql_where = {
            'parent__id': 1
        }
        
        if keyword:
            sql_where['name__icontains'] = keyword.strip()

        items = TagInfo.objects.filter(**sql_where).order_by('-created_at')
        paginator = Paginator(items, page_size, request=request, pre_name=u"来源")
        page = paginator.page(page_num)

        return render(request, 'tactic/kb/origin/index.html', {
            'nav': 'tactic',
            'page': page,
            'keyword': keyword,
        })
