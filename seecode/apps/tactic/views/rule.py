# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.http import urlquote
from django.views.decorators.csrf import ensure_csrf_cookie

from seecode.apps.tactic.models import TacticInfo
from seecode.libs.core.enum import COMPONENT_MATCH_TYPE
from seecode.libs.core.enum import RISK_TYPE
from seecode.libs.core.enum import TACTIC_MATCH_TYPE
from seecode.libs.core.enum import TACTIC_TYPE
from seecode.libs.core.exceptions import ParameterIsEmptyException
from seecode.libs.core.exceptions import QueryConditionIsEmptyException
from seecode.libs.core.pluginctl import dump_plugin
from seecode.libs.dal.engine import get_all_engine
from seecode.libs.dal.engine import get_engine_by_module_name
from seecode.libs.dal.lang import get_lang_all
from seecode.libs.dal.lang import get_lang_by_id
from seecode.libs.dal.tactic import bulk_delete_tactic
from seecode.libs.dal.tactic import bulk_update_tactic
from seecode.libs.dal.tactic import create_tactic_obj
from seecode.libs.dal.tactic import get_tactic_by_id
from seecode.libs.dal.tactic import get_tactic_by_key
from seecode.libs.dal.tactic import sync_sonar_rule
from seecode.libs.dal.tactic import update_tactic_obj
from seecode.libs.dal.vuln import get_vuln_by_id
from seecode.libs.paginator import Paginator
from seecode.libs.units import parse_bool
from seecode.libs.units import parse_int
from seecode.libs.units import strip


@login_required
@ensure_csrf_cookie
def index(request):
    """
    :param request:
    :return:
    """
    if request.method == "POST":
        try:
            tactic_id = request.POST.get('tactic_id', None)
            if tactic_id:
                msg = '修改策略规则成功!'
            else:
                msg = '添加策略规则成功!'
            save(request)
            return HttpResponseRedirect('/tactic/rule/?msg={0}'.format(urlquote(msg)))
        except (Exception, QueryConditionIsEmptyException, ParameterIsEmptyException) as ex:
            import traceback;
            traceback.print_exc()  # FIXME syslog
            return HttpResponseRedirect('/tactic/rule/?errmsg={0}'.format(urlquote(str(ex))))
    else:
        t = strip(request.GET.get('t', ''))
        e = strip(request.GET.get('e', ''))
        n = strip(request.GET.get('n', ''))
        r = strip(request.GET.get('r', ''))
        lang = strip(request.GET.get('l', ''))
        keyword = strip(request.GET.get('k', ''))
        a = strip(request.GET.get('a', ''))
        kb = strip(request.GET.get('kb', ''))
        page_num = parse_int(request.GET.get('p', 1), 1)
        page_size = parse_int(request.GET.get('ps', 20), 20)
        sql_where = {}
        if n:
            sql_where['nature_type'] = parse_int(n, 0)
        if t:
            sql_where['type'] = parse_int(t, 0)
        if r:
            sql_where['risk'] = parse_int(r, 0)
        if e:
            sql_where['engine__id'] = int(e)
        if keyword:
            sql_where['name__icontains'] = keyword
        if lang:
            sql_where['lang__id'] = int(lang)
        if a:
            if a == '1':
                sql_where['alarm_enable'] = True
            else:
                sql_where['alarm_enable'] = False
        if kb:
            if kb == '1':
                sql_where['vuln__isnull'] = False
            else:
                sql_where['vuln__isnull'] = True

        items = TacticInfo.objects.filter(**sql_where).order_by('-updated_at')
        paginator = Paginator(items, page_size, request=request, pre_name=u"规则")
        page = paginator.page(page_num)

        return render(request, 'tactic/rule/index.html', {
            'nav': 'tactic',
            'page': page,
            't': t,
            'r': r,
            'n': n,
            'a': a,
            'e': e,
            'kb': kb,
            'l': lang,
            'keyword': keyword,
            'risk_list': RISK_TYPE,
            'tactic_type_list': TACTIC_TYPE,
            'match_list': TACTIC_MATCH_TYPE,
            'engine_list': get_all_engine(),
            'component_match_list': COMPONENT_MATCH_TYPE,
            'lang_list': get_lang_all(),
        })


@login_required
@ensure_csrf_cookie
def show(request, tactic_id):
    """
    :param request:
    :param tactic_id:
    :return:
    """
    if request.method == 'POST':
        save(request)
        return HttpResponseRedirect("/tactic/rule/{0}/".format(tactic_id))
    else:
        kb, tags = None, ''
        model = get_tactic_by_id(tactic_id=tactic_id)
        if not model:
            return HttpResponseRedirect('/tactic/rule/?errmsg={0}'.format(urlquote('策略规则不存在!')))
        if model.vuln:
            kb = get_vuln_by_id(vuln_id=model.vuln.id)
        tag_list = model.tags.all()
        if tag_list:
            tags = [_.name.upper() for _ in tag_list]
            tags = ','.join(tags)

        return render(request, 'tactic/rule/edit.html', {
            'nav': 'tactic',
            'model': model,
            'kb': kb,
            'tags': tags,
            'risk_list': RISK_TYPE,
            'tactic_type_list': TACTIC_TYPE,
            'match_list': TACTIC_MATCH_TYPE,
            'component_match_list': COMPONENT_MATCH_TYPE,
        })


@login_required
def save(request):
    """
    :param request:
    :return:
    """
    name = strip(request.POST.get('name', None))
    key = strip(request.POST.get('key', None))
    lang_id = strip(request.POST.get('lang', None))
    tactic_id = strip(request.POST.get('tactic_id', None))

    nature_type = strip(request.POST.get('nature_type', 1))
    tactic_type = strip(request.POST.get('tactic_type', 3))
    risk = strip(request.POST.get('risk', None))
    kb_id = strip(request.POST.get('kb_id', None))
    rule_match_type = strip(request.POST.get('match_type', 0))
    file_ext = strip(request.POST.get('file_ext', None))
    component_match_type = strip(request.POST.get('component_match_type', None))
    rule_regex = strip(request.POST.get('rule_regex', None))
    component_name = strip(request.POST.get('component_name', None))
    rule_regex_flag = strip(request.POST.get('rule_regex_flag', None))

    description = strip(request.POST.get('description', ''))
    solution = strip(request.POST.get('solution', ''))
    is_active = parse_bool(strip(request.POST.get('is_active', False)))

    plugin_name = strip(request.POST.get('plugin_name', ''))
    plugin_content = strip(request.POST.get('plugin_content', ''))
    tags = strip(request.POST.get('tags', ''))

    nature_type = int(nature_type)
    tactic_type = int(tactic_type)
    rule_match_type = int(rule_match_type)
    risk = int(risk)
    vuln_obj = None
    rule_value = ''

    if kb_id:
        kb_id = int(kb_id)
        vuln_obj = get_vuln_by_id(vuln_id=kb_id)

    if not all((name, key,)):
        raise Exception('请填写"策略标题"、"Key"字段!')

    key = key.lower()

    if rule_match_type == 3:
        rule_value = file_ext
    elif rule_match_type == 4:
        rule_value = component_match_type

    plugin_module_name = ''
    if plugin_name and plugin_content:
        plugin_module_name = dump_plugin(name=plugin_name, content=plugin_content)

    if tactic_id:
        tactic_id = int(tactic_id)
        model = get_tactic_by_id(tactic_id=tactic_id)
        if not model:
            raise Exception('"tactic_id={0}"规则策略未找到!'.format(tactic_id))
        tactic_obj = get_tactic_by_key(key=key)
        if tactic_obj and tactic_obj.id != tactic_id:
            raise Exception('"{0}"已存在！'.format(key))

        update_tactic_obj(
            tactic_id=tactic_id,
            user=request.user,
            vuln_obj=vuln_obj,
            is_active=is_active,
            key=key,
            name=name,
            description=description,
            solution=solution,
            type=tactic_type,
            risk=risk,
            nature_type=nature_type,
            rule_match_type=rule_match_type,
            rule_value=rule_value,
            rule_regex=rule_regex,
            rule_regex_flag=rule_regex_flag,
            component_name=component_name,
            plugin_name=plugin_name,
            plugin_module_name=plugin_module_name,
            plugin_content=plugin_content,
            tags=tags,
        )
    else:
        engine = strip(request.POST.get('engine', None))
        if get_tactic_by_key(key=key):
            raise Exception('"{0}"已存在！'.format(key))

        lang_obj = get_lang_by_id(lang_id=lang_id)
        if engine == 'RuleScanner':
            attribution_type = 1
            engine_obj = get_engine_by_module_name(module_name='seecode_scanner.lib.engines.rulescanner')
        elif engine == 'PluginScanner':
            attribution_type = 2
            engine_obj = get_engine_by_module_name(module_name='seecode_scanner.lib.engines.pluginscanner')
        else:
            attribution_type = 3
            engine_obj = get_engine_by_module_name(module_name='seecode_scanner.lib.engines.sonarscanner')

        create_tactic_obj(
            lang_obj=lang_obj,
            engine_obj=engine_obj,
            key=key,
            name=name,
            user=request.user,
            vuln_obj=vuln_obj,
            is_active=True,
            type=tactic_type,
            risk=risk,
            nature_type=nature_type,
            attribution_type=attribution_type,
            rule_match_type=rule_match_type,
            rule_value=rule_value,
            rule_regex=rule_regex,
            rule_regex_flag=rule_regex_flag,
            component_name=component_name,
        )


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
            bulk_delete_tactic(id_list)
        elif action == 'disable':
            bulk_update_tactic(id_list, 'disable')
        elif action == 'enable':
            bulk_update_tactic(id_list, 'enable')
        elif action == 'sync-sonar-rule':
            sync_sonar_rule()

        return JsonResponse({"status": "ok"}, safe=False)
    except Exception as ex:
        import traceback;
        traceback.print_exc()
        return JsonResponse({"status": "failed", 'msg': ex.__repr__()}, safe=False)


@login_required
@ensure_csrf_cookie
def verify_regex(request):
    """
       :param request:
       :return:
       """
    result = {"status": "ok"}
    content = strip(request.POST.get('content', None))
    role = request.POST.get('role', None)

    if role == 'file_ext':
        if content and ',' in content:
            ext_list = content.split(',')
            for item in ext_list:
                if not item.startswith('.'):
                    result['status'] = 'failed'
                    result['msg'] = '多个文件名后缀必须使用英文的(,)隔开, 以(.)开始!'
                    break

    else:
        if content:
            regex_list = content.split('\n')
            try:
                for item in regex_list:
                    re.compile(item)
            except re.error as ex:
                result['status'] = 'failed'
                result['msg'] = '正则表达式不正确, 请输入正确的正则表达式!'

    return JsonResponse(result, safe=False)


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
            result_list = TacticInfo.objects.filter(key=keyword.strip()).first()
            if result_list:
                return JsonResponse(
                    {"status": 1, 'msg': "您输入的 \"{0}\" Key已存在，请从新输入。".format(keyword.strip())},
                    safe=False
                )
            else:
                return JsonResponse({"status": 0, 'msg': "当前Key不存在。"}, safe=False)

    except Exception as ex:
        import traceback;
        traceback.print_exc()
        return JsonResponse({"status": "failed", 'msg': str(ex)}, safe=False)
