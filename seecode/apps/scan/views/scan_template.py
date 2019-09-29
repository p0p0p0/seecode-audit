# coding: utf-8
from __future__ import unicode_literals

import ast

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.utils.http import urlquote
from django.views.decorators.csrf import ensure_csrf_cookie

from seecode.apps.scan.models import ScanProfileInfo
from seecode.apps.tactic.models import TacticInfo
from seecode.libs.core.enum import SONAR_PROJECT_PROPERTIES
from seecode.libs.core.enum import TACTIC_TYPE
from seecode.libs.dal.engine import get_all_engine
from seecode.libs.dal.engine import get_engine_by_id
from seecode.libs.dal.scan_profile import clean_engine_cache
from seecode.libs.dal.scan_profile import create_profile_obj
from seecode.libs.dal.scan_profile import delete_profile
from seecode.libs.dal.scan_profile import get_profile_by_id
from seecode.libs.dal.scan_profile import get_profile_by_name
from seecode.libs.dal.scan_profile import update_profile_obj
from seecode.libs.dal.tactic import get_tactic_by_id
from seecode.libs.dal.tactic import get_tactic_plugin_all
from seecode.libs.dal.tactic import get_tactic_rule_all
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
            action = request.POST.get('action', '')
            if action == 'del':
                ids = request.POST.get('ids', '')
                if action and 'del' == action:
                    profile_list = [_ for _ in ids.split(',') if _]
                    for item in profile_list:
                        delete_profile(profile_id=item)
                    return JsonResponse({'status': 'ok'}, safe=False)
            else:
                result = save(request)
                name = request.POST.get('name', '')
                if result == 1:
                    msg = urlquote('修改 "{0}" 模板成功!'.format(name))
                else:
                    msg = urlquote('创建 "{0}" 模板成功!'.format(name))
                return HttpResponseRedirect('/scan/template/?msg={0}'.format(msg))
        except Exception as ex:
            import traceback;traceback.print_exc()
            return HttpResponseRedirect('/scan/template/?errmsg={0}'.format(urlquote(str(ex))))
    else:
        keyword = request.GET.get('k', '')
        page_num = parse_int(request.GET.get('p', 1), 1)
        page_size = parse_int(request.GET.get('ps', 20), 20)
        sql_where = {}
        if keyword:
            keyword = keyword.strip()
            sql_where['name__icontains'] = keyword

        items = ScanProfileInfo.objects.filter(**sql_where).order_by('-created_at')
        paginator = Paginator(items, page_size, request=request, pre_name=u"扫描模板")
        page = paginator.page(page_num)

        return render(request, 'scan/template/index.html', {
            'nav': 'scan',
            'page': page,
            'keyword': keyword,
            'engines': get_all_engine,
        })


@login_required
@ensure_csrf_cookie
def show(request, profile_id):
    """
    :param request:
    :param profile_id:
    :return:
    """
    model = get_profile_by_id(profile_id=profile_id)
    template_conf = None
    if not model:
        return HttpResponseRedirect('/scan/template/?errmsg={0}'.format(urlquote('扫描模板未找到!')))
    if model.config:
        template_conf = ast.literal_eval(model.config)

    return render(request, 'scan/template/edit.html', {
        'nav': 'scan',
        'model': model,
        'engines': get_all_engine(),
        'rule_list': get_tactic_rule_all(),
        'plugin_list': get_tactic_plugin_all(),
        'template_conf': template_conf,
        'statistics': TACTIC_TYPE,
    })


@login_required
def save(request):
    """
    :param request:
    :return:
    """
    result = None
    name = request.POST.get('name', '')
    description = request.POST.get('description', '')
    exclude_dir = request.POST.get('exclude_dir', '')
    exclude_ext = request.POST.get('exclude_ext', '')
    exclude_file = request.POST.get('exclude_file', '')
    exclude_java_package = request.POST.get('exclude_java_package', '')
    task_timeout = request.POST.get('task_timeout', '')

    enable_auto_ignore = parse_bool(request.POST.get('enable_auto_ignore', False))
    enable_commit_issue = parse_bool(request.POST.get('enable_commit_issue', False))
    is_rule_all = parse_bool(request.POST.get('rule_all', False))
    is_plugin_all = parse_bool(request.POST.get('plugin_all', False))

    engine_list = request.POST.getlist('engine', '')
    profile_id = request.POST.get('profile_id', '')

    if not all((name, engine_list)):
        raise Exception('"name, engine_list"参数不能为空!')

    if profile_id:
        pluginscanner_k = request.POST.getlist('seecode_scanner.lib.engines.pluginscanner_key')
        pluginscanner_v = request.POST.getlist('seecode_scanner.lib.engines.pluginscanner_value')
        rulescanner_k = request.POST.getlist('seecode_scanner.lib.engines.rulescanner_key')
        rulescanner_v = request.POST.getlist('seecode_scanner.lib.engines.rulescanner_value')
        sonarscanner_k = request.POST.getlist('seecode_scanner.lib.engines.sonarscanner_key')
        sonarscanner_v = request.POST.getlist('seecode_scanner.lib.engines.sonarscanner_value')
        data = {
            'seecode_scanner.lib.engines.pluginscanner': {
                'ENGINE_TIMEOUT': 1200,
            },
            'seecode_scanner.lib.engines.rulescanner': {
                'ENGINE_TIMEOUT': 1200,
                'FILE_SIZE_LIMIT': 5120,
            },
            'seecode_scanner.lib.engines.sonarscanner': {
                'HTTP_TIMEOUT': 10,
                'HTTP_TIMEOUT_RETRY': 3,
                'HTTP_FAILED_RETRY': 3,
                'SONAR_PROJECT_PROPERTIES': SONAR_PROJECT_PROPERTIES,
                'ENGINE_TIMEOUT': 1200,
            },
        }
        for i in range(0, len(pluginscanner_k)):
            data['seecode_scanner.lib.engines.pluginscanner'][pluginscanner_k[i]] = pluginscanner_v[i]
        for i in range(0, len(rulescanner_k)):
            data['seecode_scanner.lib.engines.rulescanner'][rulescanner_k[i]] = rulescanner_v[i]
        for i in range(0, len(sonarscanner_k)):
            data['seecode_scanner.lib.engines.sonarscanner'][sonarscanner_k[i]] = sonarscanner_v[i]

        pro_obj = update_profile_obj(
            profile_id=profile_id,
            name=name,
            description=description,
            exclude_dir=exclude_dir,
            exclude_ext=exclude_ext,
            exclude_file=exclude_file,
            exclude_java_package=exclude_java_package,
            enable_commit_issue=enable_commit_issue,
            enable_auto_ignore=enable_auto_ignore,
            task_timeout=task_timeout,
        )
        template_config = ast.literal_eval(pro_obj.config)
        for item in engine_list:
            engine_obj = get_engine_by_id(engine_id=item)
            if engine_obj:
                pro_obj.engines.add(engine_obj)
                if engine_obj.module_name not in template_config:
                    template_config[engine_obj.module_name] = {}

                if engine_obj.module_name == 'seecode_scanner.lib.engines.sonarscanner':
                    template_config[engine_obj.module_name]['HTTP_TIMEOUT'] = data[engine_obj.module_name]['HTTP_TIMEOUT']
                    template_config[engine_obj.module_name]['HTTP_TIMEOUT_RETRY'] = data[engine_obj.module_name]['HTTP_TIMEOUT_RETRY']
                    template_config[engine_obj.module_name]['HTTP_FAILED_RETRY'] = data[engine_obj.module_name]['HTTP_FAILED_RETRY']
                    template_config[engine_obj.module_name]['SONAR_PROJECT_PROPERTIES'] = data[engine_obj.module_name]['SONAR_PROJECT_PROPERTIES']
                    template_config[engine_obj.module_name]['ENGINE_TIMEOUT'] = data[engine_obj.module_name]['ENGINE_TIMEOUT']

                elif is_rule_all and engine_obj.module_name == 'seecode_scanner.lib.engines.rulescanner':
                    template_config[engine_obj.module_name]['FILE_SIZE_LIMIT'] = data[engine_obj.module_name]['FILE_SIZE_LIMIT']
                    template_config[engine_obj.module_name]['ENGINE_TIMEOUT'] = data[engine_obj.module_name]['ENGINE_TIMEOUT']

                elif is_plugin_all and engine_obj.module_name == 'seecode_scanner.lib.engines.pluginscanner':
                    template_config[engine_obj.module_name]['ENGINE_TIMEOUT'] = data[engine_obj.module_name]['ENGINE_TIMEOUT']
            if pro_obj:
                pro_obj.config = str(template_config)
                pro_obj.save()
        result = 1
    else:
        pro_obj = get_profile_by_name(name=name)
        if pro_obj:
            raise Exception('"{0}"扫描策略已存在!'.format(name))

        pro_obj = create_profile_obj(
            name=name,
            exclude_dir=exclude_dir,
            exclude_ext=exclude_ext,
            exclude_file=exclude_file,
            exclude_java_package=exclude_java_package,
            description=description,
            enable_auto_ignore=enable_auto_ignore,
            enable_commit_issue=enable_commit_issue,
            task_timeout=task_timeout,
        )
        template_config = {}
        for item in engine_list:
            engine_obj = get_engine_by_id(engine_id=item)
            if engine_obj:
                pro_obj.engines.add(engine_obj)
                template_config[engine_obj.module_name] = {
                    'ENGINE_TIMEOUT': 60 * 20,  # minute
                }
                if engine_obj.module_name == 'seecode_scanner.lib.engines.sonarscanner':
                    template_config[engine_obj.module_name]['HTTP_TIMEOUT'] = 10
                    template_config[engine_obj.module_name]['HTTP_TIMEOUT_RETRY'] = 3
                    template_config[engine_obj.module_name]['HTTP_FAILED_RETRY'] = 3
                    template_config[engine_obj.module_name]['SONAR_PROJECT_PROPERTIES'] = SONAR_PROJECT_PROPERTIES
                    items = TacticInfo.objects.filter(is_active=True, engine__id=engine_obj.id)
                    pro_obj.tactics.add(*items)

                elif is_rule_all and engine_obj.module_name == 'seecode_scanner.lib.engines.rulescanner':
                    template_config[engine_obj.module_name]['FILE_SIZE_LIMIT'] = 1024 * 5  # KB
                    items = TacticInfo.objects.filter(attribution_type=1, is_active=True, engine__id=engine_obj.id)
                    pro_obj.tactics.add(*items)

                elif is_plugin_all and engine_obj.module_name == 'seecode_scanner.lib.engines.pluginscanner':
                    items = TacticInfo.objects.filter(attribution_type=2, is_active=True)
                    pro_obj.tactics.add(*items)

        if pro_obj:
            pro_obj.config = str(template_config)
            pro_obj.save()
        result = 2
    return result


@login_required
@ensure_csrf_cookie
def tactic(request):
    """
    :param request:
    :return:
    """
    profile_id = request.POST.get('profile_id', None)
    tactic_type = request.POST.get('tactic_type', None)
    selected_rule = request.POST.get('selected_rule', None)

    if not all((profile_id, tactic_type, selected_rule)):
        raise Exception('"profile_id, tactic_type, selected_rule"参数不能为空!')

    if profile_id:
        profile_obj = get_profile_by_id(profile_id=profile_id)

        if tactic_type == 'rule':
            rule_id_list = selected_rule.split(',')
            profile_obj.rules.remove()
            for item in rule_id_list:
                obj = get_tactic_by_id(tactic_id=int(item))
                if obj:
                    profile_obj.rules.add(obj)
        else:
            plugin_id_list = selected_rule.split(',')
            profile_obj.plugins.remove()
            for item in plugin_id_list:
                obj = get_tactic_by_id(tactic_id=int(item))
                if obj:
                    profile_obj.plugins.add(obj)
        clean_engine_cache(profile_id=profile_obj.id)
    return HttpResponseRedirect('/scan/template/{0}/'.format(profile_id))


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
            result_list = ScanProfileInfo.objects.filter(name=keyword.strip()).first()
            if result_list:
                return JsonResponse({"status": 1, 'msg': "您输入的 \"{0}\" 扫描模板名称已存在，请从新输入。".format(keyword.strip())}, safe=False)
            else:
                return JsonResponse({"status": 0, 'msg': "当前扫描模板名称不存在。"}, safe=False)

    except Exception as ex:
        import traceback;
        traceback.print_exc()
        return JsonResponse({"status": "failed", 'msg': str(ex)}, safe=False)
