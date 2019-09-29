# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.http import urlquote
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie

from seecode.apps.system.models import LanguageInfo
from seecode.libs.dal.lang import create_lang_obj, get_lang_by_key, get_lang_by_name
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
            lang_obj = None
            action = request.POST.get('action', None)
            if action == 'del':
                ids = request.POST.get('ids', None)
                LanguageInfo.objects.filter(id__in=[_ for _ in ids.split(',') if _]).delete()
                return HttpResponseRedirect('/sys/lang/')
            else:
                name = request.POST.get('name', None)
                key = request.POST.get('key', None)
                if not name:
                    raise Exception('语言名称不能为空!')
                if key:
                    lang_obj = get_lang_by_key(key=key)
                if name:
                    lang_obj = get_lang_by_name(name=name)
                if lang_obj:
                    raise Exception('开发语言已存在!')
                create_lang_obj(name=name, key=key)

                return HttpResponseRedirect('/sys/lang/?msg={0}'.format(urlquote('添加成功!')))
        except Exception as ex:
            return HttpResponseRedirect('/sys/lang/?errmsg={0}'.format(urlquote(ex)))
    else:
        keyword = request.GET.get('k', '')

        page_num = parse_int(request.GET.get('p', 1), 1)
        page_size = parse_int(request.GET.get('ps', 20), 20)

        sql_where = {}

        if keyword:
            sql_where['name__icontains'] = keyword.strip()

        items = LanguageInfo.objects.filter(**sql_where).order_by('-created_at')
        paginator = Paginator(items, page_size, request=request, pre_name=u"语言")
        page = paginator.page(page_num)

        return render(request, 'system/lang/index.html', {
            'nav': 'sys',
            'page': page,
            'keyword': keyword,
        })


@login_required
@ensure_csrf_cookie
def show(request, lang_id):
    """
    :param request:
    :param lang_id:
    :return:
    """
    try:
        model = LanguageInfo.objects.get(id=lang_id)

    except LanguageInfo.DoesNotExist as ex:
        model = None

    return render(request, 'system/lang/edit.html', {
        'nav': 'sys',
        'model': model,
    })

