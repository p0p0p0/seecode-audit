# coding: utf-8
from __future__ import unicode_literals

from django.core.cache import cache
from django.db.models import Count

from seecode.libs.core.data import logger
from seecode.apps.project.models.app import ApplicationInfo
from seecode.apps.scan.models import IssueInfo
from seecode.libs.dal.lang import get_lang_by_name
from seecode.libs.core.common import parse_int
from seecode.libs.units import close_old_connections
from seecode.libs.core.exceptions import ParameterIsEmptyException
from seecode.libs.core.exceptions import QueryConditionIsEmptyException
from seecode.libs.core.cache_key import PROJECT_APP_CACHE
from seecode.libs.core.common import get_project_scope


def create_app_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    project_obj = kwargs.get('project_obj', None)
    repo_obj = kwargs.get('repo_obj', None)
    lang_obj = kwargs.get('lang_obj', None)
    module_name = kwargs.get('module_name', None)
    app_name = kwargs.get('app_name', None)
    version = kwargs.get('version', '')
    code_total = parse_int(kwargs.get('code_total', 0))
    size = parse_int(kwargs.get('size', 0))
    report_url = kwargs.get('report_url', '')
    ignore_count = parse_int(kwargs.get('ignore_count', 0))
    critical = parse_int(kwargs.get('critical', 0))
    high = parse_int(kwargs.get('high', 0))
    medium = parse_int(kwargs.get('medium', 0))
    low = parse_int(kwargs.get('low', 0))
    info = parse_int(kwargs.get('info', 0))
    status = kwargs.get('info', 1)

    if not all((project_obj, module_name, app_name, )):
        raise ParameterIsEmptyException(u'"project_obj, module_name, app_name" parameters cannot be empty !')

    module_name = module_name.lower()

    close_old_connections()

    app = ApplicationInfo(
        project=project_obj,
        repo=repo_obj,
        lang=lang_obj,
        module_name=module_name.strip(),
        app_name=app_name.strip(),
        version=version,
        code_total=code_total,
        size=size,
        report_url=report_url,
        ignore_count=ignore_count,
        critical=critical,
        high=high,
        medium=medium,
        low=low,
        info=info,
        risk_scope=0,
        status=status,
    )
    app.save()
    return app


def _get_app_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    result = None
    app_id = kwargs.get('app_id', None)
    module_name = kwargs.get('module_name', None)
    app_name = kwargs.get('app_name', None)
    project_id = kwargs.get('project_id', None)
    close_old_connections()

    try:
        sql_where = {}
        if app_id:
            sql_where['id'] = int(app_id)
        if project_id:
            sql_where['project__id'] = int(project_id)
        if module_name:
            sql_where['module_name__iexact'] = module_name.lower().strip()
        if app_name:
            sql_where['app_name__iexact'] = app_name.strip()

        if not sql_where:
            raise QueryConditionIsEmptyException(u'Missing "app_id, module_name, app_name" key parameters!')

        item = ApplicationInfo.objects.filter(**sql_where).first()
        result = item
    except ApplicationInfo.DoesNotExist as ex:
        logger.warning(ex)
    return result


def update_app_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    result = None
    app_id = kwargs.get('app_id', None)
    repo_obj = kwargs.get('repo_obj', None)
    lang_obj = kwargs.get('lang_obj', None)
    module_name = kwargs.get('module_name', None)
    app_name = kwargs.get('app_name', None)
    version = kwargs.get('version', '')
    code_total = kwargs.get('code_total', None)
    size = kwargs.get('size', None)
    report_url = kwargs.get('report_url', '')
    ignore_count = kwargs.get('ignore_count', None)
    critical = parse_int(kwargs.get("critical", 0))
    high = parse_int(kwargs.get("high", 0))
    medium = parse_int(kwargs.get("medium", 0))
    low = parse_int(kwargs.get("low", 0))
    info = parse_int(kwargs.get("info", 0))
    scope = kwargs.get('scope', 0)
    status = kwargs.get('status', None)
    last_scan_time = kwargs.get('last_scan_time', None)

    try:
        sql_where = {}

        if app_id:
            sql_where['id'] = int(app_id)
        if module_name:
            sql_where['module_name'] = module_name.lower().strip()

        if not sql_where:
            raise QueryConditionIsEmptyException(u'Missing "app_id, module_name" key parameters!')

        item = ApplicationInfo.objects.filter(**sql_where).first()
        if item:
            if repo_obj:
                item.repo = repo_obj
            if lang_obj:
                item.lang = lang_obj
            if app_name:
                item.app_name = app_name.strip()
            if version:
                item.version = version.strip()
            if code_total and code_total > 0:
                item.code_total = int(code_total)
            if size and size > 0:
                item.size = int(size) * 1024
            if report_url:
                item.report_url = report_url.strip()
            if ignore_count and ignore_count> 0:
                item.ignore_count = int(ignore_count)
            if critical and critical > 0:
                item.critical = int(critical)
            if high and high > 0:
                item.high = int(high)
            if medium and medium > 0:
                item.medium = int(medium)
            if low and low > 0:
                item.low = int(low)
            if info and info > 0:
                item.info = int(info)
            if scope:
                item.risk_scope = round(float(scope), 2)
            if last_scan_time:
                item.last_scan_time = last_scan_time
            if status:
                item.status = int(status)

            item.save()
            cache.set('{0}:{1}'.format(PROJECT_APP_CACHE[1], app_id), None, 0)
            cache.set('{0}:{1}'.format(PROJECT_APP_CACHE[4], app_id), None, 0)
            result = item
    except ApplicationInfo.DoesNotExist as ex:
        logger.warning(ex)
    return result


def update_app_lang(**kwargs):
    """

    :param kwargs:
    :return:
    """
    result = False
    app_id = kwargs.get('app_id', None)
    lang = kwargs.get('lang', None)
    size = kwargs.get('size', None)
    status = kwargs.get('status', None)
    code_total = kwargs.get('code_total', None)

    try:
        if lang:
            lang_obj = get_lang_by_name(name=lang)
            result = update_app_obj(
                app_id=app_id,
                lang_obj=lang_obj,
                size=size,
                code_total=code_total,
                status=status,
            )
    except Exception as ex:
        logger.warning(ex)
    return result


def update_app_statistics(**kwargs):
    """

    :param kwargs:
    :return:
    """
    app_id = kwargs.get("app_id")
    critical = parse_int(kwargs.get("critical", 0))
    high = parse_int(kwargs.get("high", 0))
    medium = parse_int(kwargs.get("medium", 0))
    low = parse_int(kwargs.get("low", 0))
    info = parse_int(kwargs.get("info", 0))
    scope = kwargs.get("scope")

    return update_app_obj(
        app_id=app_id,
        critical=critical,
        high=high,
        medium=medium,
        low=low,
        info=info,
        scope=scope,
    )


def get_app_by_id(app_id):
    """

    :param app_id:
    :return:
    """
    cache_key = '{0}:{1}'.format(PROJECT_APP_CACHE[1], app_id)
    cache_obj = cache.get(cache_key)
    if cache_obj:
        return cache_obj
    obj = _get_app_obj(app_id=app_id)
    if obj:
        cache.set(cache_key, obj, PROJECT_APP_CACHE[0])
    return obj


def get_app_risk_by_id(app_id):
    """

    :param app_id:
    :return:
    """

    cache_key = '{0}:{1}'.format(PROJECT_APP_CACHE[4], app_id)
    cache_obj = cache.get(cache_key)
    if cache_obj:
        return cache_obj
    obj = get_app_by_id(app_id=app_id)
    result = {
        'bug': {
            'critical': 0,
            'high': 0,
            'medium': 0,
            'low': 0,
            'info': 0,
        },
        'code_smell': {
            'critical': 0,
            'high': 0,
            'medium': 0,
            'low': 0,
            'info': 0,
        },
        'vulnerability': {
            'critical': obj.critical,
            'high': obj.high,
            'medium': obj.medium,
            'low': obj.low,
            'info': obj.info,
        }
    }

    # FIXME
    _result = {
        'bug': {
            '1': 0,
            '2': 0,
            '3': 0,
            '4': 0,
        },
        'code smell': {
            '1': 0,
            '2': 0,
            '3': 0,
            '4': 0,
        },
        'vulnerability': {
            '1': obj.critical,
            '2': obj.high,
            '3': obj.medium,
            '4': obj.low,
        }
    }

    # bug
    bugs = IssueInfo.objects.filter(app__id=app_id, tactic__type=1, status=1).values('tactic__risk').annotate(total=Count('tactic__risk'))
    for item in bugs:
        if item['tactic__risk'] == 1:
            result['bug']['critical'] = item['total']
            _result['bug']['1'] = item['total']
        elif item['tactic__risk'] == 2:
            result['bug']['high'] = item['total']
            _result['bug']['2'] = item['total']
        elif item['tactic__risk'] == 3:
            result['bug']['medium'] = item['total']
            _result['bug']['3'] = item['total']
        elif item['tactic__risk'] == 4:
            result['bug']['low'] = item['total']
            _result['bug']['4'] = item['total']
        elif item['tactic__risk'] == 5:
            result['bug']['info'] = item['total']
    # code_smell
    code_smells = IssueInfo.objects.filter(app__id=app_id, tactic__type=2, status=1).values('tactic__risk').annotate(total=Count('tactic__risk'))
    for item in code_smells:
        if item['tactic__risk'] == 1:
            result['code_smell']['critical'] = item['total']
            _result['code smell']['1'] = item['total']
        elif item['tactic__risk'] == 2:
            result['code_smell']['high'] = item['total']
            _result['code smell']['2'] = item['total']
        elif item['tactic__risk'] == 3:
            result['code_smell']['medium'] = item['total']
            _result['code smell']['3'] = item['total']
        elif item['tactic__risk'] == 4:
            result['code_smell']['low'] = item['total']
            _result['code smell']['4'] = item['total']
        elif item['tactic__risk'] == 5:
            result['code_smell']['info'] = item['total']

    scope = get_project_scope(_result)
    update_app_obj(
        app_id=app_id,
        scope=scope
    )
    cache.set(cache_key, result, PROJECT_APP_CACHE[0])
    return result


def get_app_by_app_name(name, project_id):
    """

    :param name:
    :param project_id:
    :return:
    """
    if not all((name, project_id, )):
        raise ParameterIsEmptyException(u'"project_id, name" parameters cannot be empty !')

    return _get_app_obj(app_name=name, project_id=project_id)


def get_app_by_module_name(name, project_id):
    """

    :param name:
    :param project_id:
    :return:
    """
    if not all((name, project_id, )):
        raise ParameterIsEmptyException(u'"project_id, name" parameters cannot be empty !')

    return _get_app_obj(module_name=name, project_id=project_id)


def get_app_by_branch(name, project_id):
    """

    :param name:
    :param project_id:
    :return:
    """
    if not all((name, project_id, )):
        raise ParameterIsEmptyException(u'"project_id, name" parameters cannot be empty !')

    sql_where = {
        'repo__name': name.strip(),
        'project__id': project_id
    }

    return ApplicationInfo.objects.filter(**sql_where).order_by('-created_at').first()


def delete_app_list(id_list):
    """

    :param id_list:
    :return:
    """
    if id_list:
        app_list = ApplicationInfo.objects.filter(id__in=id_list)
        for item in app_list:
            cache_key = '{0}:{1}'.format(PROJECT_APP_CACHE[1], item.id)
            cache.set(cache_key, None, 0)
            item.delete()
