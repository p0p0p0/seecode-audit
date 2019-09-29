# coding: utf-8
from __future__ import unicode_literals

import ast
from decimal import Decimal

from django.core.cache import cache
from markdownify import markdownify as md

from seecode.apps.tactic.models import TacticInfo
from seecode.libs.core.cache_key import TACTIC_CACHE
from seecode.libs.core.common import get_issue_type_by_sonar
from seecode.libs.core.common import get_risk_by_severity
from seecode.libs.core.data import logger
from seecode.libs.core.enum import action
from seecode.libs.core.enum import changelog_module
from seecode.libs.core.exceptions import ParameterIsEmptyException
from seecode.libs.core.exceptions import QueryConditionIsEmptyException
from seecode.libs.dal.engine import get_engine_by_module_name
from seecode.libs.dal.lang import get_lang_by_key
from seecode.libs.dal.tag import bulk_tag
from seecode.libs.dal.upgrade_version import update_client_minor_version
from seecode.libs.dal.upgrade_version import update_client_revision_version
from seecode.libs.units import close_old_connections
from seecode.libs.units import get_tactic_risk_scope
from seecode.libs.units import get_tactic_tag_scope
from seecode.libs.units import get_tactic_type_scope
from seecode.libs.units import get_scope_level
from seecode.libs.utils.api_sonarqube import SonarAPIHandler


def create_tactic_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    lang_obj = kwargs.get('lang_obj', None)
    engine_obj = kwargs.get('engine_obj', None)
    vuln_obj = kwargs.get('vuln_obj', None)
    user = kwargs.get('user', None)
    is_active = kwargs.get('is_active', True)
    key = kwargs.get('key', '')
    name = kwargs.get('name', '')
    description = kwargs.get('description', '')
    tactic_type = kwargs.get('type', 2)
    risk = kwargs.get('risk', 3)
    nature_type = kwargs.get('nature_type', 1)
    attribution_type = kwargs.get('attribution_type', 1)
    rule_match_type = kwargs.get('rule_match_type', 1)
    rule_value = kwargs.get('rule_value', '')
    rule_regex = kwargs.get('rule_regex', '')
    rule_regex_flag = kwargs.get('rule_regex_flag', '')
    component_name = kwargs.get('component_name', '')
    plugin_name = kwargs.get('plugin_name', '')
    plugin_path = kwargs.get('plugin_path', '')
    plugin_content = kwargs.get('plugin_content', '')

    if not all((engine_obj, name, key, )):
        raise ParameterIsEmptyException(u'"engine_obj, name, key" parameters cannot be empty !')

    if name and len(name) > 255:
        name = name[:255]

    # scope
    r_s = get_tactic_type_scope(tactic_type)
    r_r = get_tactic_risk_scope(risk)
    r_t = 0
    # （类型权重+风险因素）* (标签系数*N) + （类型权重+风险因素）
    risk_scope = (r_s + r_r) * r_t + (r_s + r_r)

    close_old_connections()
    tactic = TacticInfo(
        lang=lang_obj,
        engine=engine_obj,
        user=user,
        vuln=vuln_obj,
        is_active=is_active,
        key=key,
        name=name,
        description=description,
        type=tactic_type,
        risk=risk,
        nature_type=nature_type,
        attribution_type=attribution_type,
        rule_match_type=rule_match_type,
        rule_value=rule_value,
        rule_regex=rule_regex,
        component_name=component_name,
        rule_regex_flag=rule_regex_flag,
        plugin_name=plugin_name,
        plugin_module_name=plugin_path,
        plugin_content=plugin_content,
        revision=0.01,
        risk_scope=risk_scope
    )
    tactic.save()
    update_client_minor_version(
        action=1,
        module=2,
        description='添加“{0}”扫描规则。'.format(key)
    )
    return tactic


def _get_tactic_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    result = None
    tactic_id = kwargs.get('tactic_id', None)
    name = kwargs.get('name', None)
    key = kwargs.get('key', None)
    attribution_type = kwargs.get('attribution_type', None)

    close_old_connections()

    try:
        sql_where = {}
        if tactic_id:
            sql_where['id'] = int(tactic_id)
        if name:
            sql_where['name'] = name
        if key:
            sql_where['key'] = key
        if attribution_type:
            sql_where['attribution_type'] = int(attribution_type)
        if not sql_where:
            raise QueryConditionIsEmptyException(u'Missing "tactic_id, name, key" key parameters!')

        result = TacticInfo.objects.filter(**sql_where).first()
    except TacticInfo.DoesNotExist as ex:
        logger.warning(ex)
    return result


def update_tactic_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    result = None
    tactic_id = kwargs.get('tactic_id', None)
    lang_obj = kwargs.get('lang_obj', None)
    engine_obj = kwargs.get('engine_obj', None)
    vuln_obj = kwargs.get('vuln_obj', None)
    user = kwargs.get('user', None)
    is_active = kwargs.get('is_active', True)
    key = kwargs.get('key', None)
    name = kwargs.get('name', None)
    description = kwargs.get('description', '')
    solution = kwargs.get('solution', '')
    tactic_type = kwargs.get('type', None)
    risk = kwargs.get('risk', None)
    nature_type = kwargs.get('nature_type', '')
    rule_match_type = kwargs.get('rule_match_type', None)
    rule_value = kwargs.get('rule_value', None)
    rule_regex = kwargs.get('rule_regex', None)
    rule_regex_flag = kwargs.get('rule_regex_flag', None)
    component_name = kwargs.get('component_name', None)
    plugin_name = kwargs.get('plugin_name', None)
    plugin_module_name = kwargs.get('plugin_module_name', None)
    plugin_content = kwargs.get('plugin_content', '')
    tags = kwargs.get('tags', None)

    try:
        sql_where = {}
        if tactic_id:
            sql_where['id'] = int(tactic_id)

        if not sql_where:
            raise QueryConditionIsEmptyException(u'Missing "tactic_id" key parameters!')

        item = TacticInfo.objects.get(**sql_where)
        if item:
            if lang_obj:
                item.lang = lang_obj
            if engine_obj:
                item.engine = engine_obj
            if is_active:
                item.is_active = True
            else:
                item.is_active = False
            if risk:
                item.risk = int(risk)
            if tactic_type:
                item.type = int(tactic_type)
            if key:
                item.key = key.lower().strip()
            if name:
                item.name = name.strip()
            if nature_type:
                item.nature_type = int(nature_type)
            if rule_match_type:
                item.rule_match_type = rule_match_type
                item.rule_value = rule_value.strip()
            if rule_regex:
                item.rule_regex = rule_regex.strip()
            if rule_regex_flag:
                rule_regex_flag = rule_regex_flag.strip()
            item.rule_regex_flag = rule_regex_flag
            if plugin_name:
                item.plugin_name = plugin_name.strip()
            if plugin_module_name:
                item.plugin_module_name = plugin_module_name.strip()
            if component_name:
                item.component_name = component_name
            item.plugin_content = plugin_content.strip()
            item.description = description
            item.solution = solution
            if user:
                item.user = user
            item.vuln = vuln_obj
            item.revision += Decimal(0.01)
            if tags:
                item.tags.clear()
                result = bulk_tag(tags, 3)
                item.tags.add(*result)
            result = item
            r_s = get_tactic_type_scope(item.type)
            r_r = get_tactic_risk_scope(item.risk)
            r_t = get_tactic_tag_scope(get_tactic_tags_by_id(item.id))
            # （类型权重+风险因素）* (标签系数*N) + （类型权重+风险因素）
            item.risk_scope = (r_s + r_r) * r_t + (r_s + r_r)
            item.save()
            cache.set('{0}:{1}'.format(TACTIC_CACHE[1], item.id), None, 0)
            cache.set('{0}:{1}'.format(TACTIC_CACHE[2], item.id), None, 0)
            update_client_revision_version(
                action=3,
                module=2,
                description='修改“{0}”扫描规则。'.format(item.key)
            )
    except TacticInfo.DoesNotExist as ex:
        logger.warning(ex)
    return result


def get_tactic_by_id(tactic_id):
    """

    :param tactic_id:
    :return:
    """
    cache_key = '{0}:{1}'.format(TACTIC_CACHE[1], tactic_id)
    cache_obj = cache.get(cache_key)
    if cache_obj:
        return cache_obj
    obj = _get_tactic_obj(tactic_id=tactic_id)
    if obj:
        cache.set(cache_key, obj, TACTIC_CACHE[0])
    return obj


def get_tactic_by_key(key):
    """

    :param key:
    :return:
    """
    cache_key = '{0}:{1}'.format(TACTIC_CACHE[1], key)
    cache_obj = cache.get(cache_key)
    if cache_obj:
        return cache_obj
    obj = _get_tactic_obj(key=key)
    if obj:
        cache.set(cache_key, obj, TACTIC_CACHE[0])
    return obj


def get_tactic_by_name(name):
    """

    :param name:
    :return:
    """
    obj = _get_tactic_obj(name=name)
    return obj


def get_tactic_rule_all():
    """

    :return:
    """
    return TacticInfo.objects.filter(attribution_type=1)


def get_tactic_plugin_all():
    """

    :return:
    """
    return TacticInfo.objects.filter(attribution_type=2)


def get_tactic_tags_by_id(tactic_id):
    """

    :return:
    """
    result = []
    cache_key = '{0}:{1}'.format(TACTIC_CACHE[2], tactic_id)
    cache_obj = cache.get(cache_key)
    if cache_obj:
        return cache_obj
    obj = get_tactic_by_id(tactic_id=tactic_id)
    if obj:
        tags = obj.tags.all()
        for tag in tags:
            if tag.name.upper() not in result:
                result.append(tag.name.lower())
        cache.set(cache_key, result, TACTIC_CACHE[0])
    return result


def bulk_delete_tactic(tactics_id):
    """

    :param tactics_id:
    :return:
    """
    tactic_list = TacticInfo.objects.filter(id__in=tactics_id)
    for item in tactic_list:
        cache.set('{0}:{1}:{2}'.format(TACTIC_CACHE[1], item.attribution_type, item.id), None, 0)

    update_client_minor_version(
        action=action.DEL,
        module=changelog_module.SCAN_TACTIC,
        description='删除“{0}”扫描规则。'.format([_.key for _ in tactic_list])
    )

    tactic_list.delete()


def bulk_update_tactic(tactics_id, ops='enable'):
    """

    :param tactics_id:
    :param ops:
    :return:
    """

    tactic_list = TacticInfo.objects.filter(id__in=tactics_id)
    tactic_type = None
    for item in tactic_list:
        cache.set('{0}:{1}:{2}'.format(TACTIC_CACHE[1], item.attribution_type, item.id), None, 0)
    if ops == 'enable':
        update_client_revision_version(
            action=action.UPDATE,
            module=changelog_module.SCAN_TACTIC,
            description='修改“{0}”扫描规则。'.format([_.key for _ in tactic_list], tactic_type)
        )
        tactic_list.update(is_active=True)
    else:
        update_client_revision_version(
            action=action.UPDATE,
            module=changelog_module.SCAN_TACTIC,
            description='修改“{0}”扫描规则。'.format([_.key for _ in tactic_list], tactic_type)
        )
        tactic_list.update(is_active=False)


def sync_sonar_rule():
    """

    :return:
    """
    sonar_engine = get_engine_by_module_name("seecode_scanner.lib.engines.sonarscanner")
    if sonar_engine:
        sonar_paramters = ast.literal_eval(sonar_engine.config)
        sonar = SonarAPIHandler(token=sonar_paramters['API_TOKEN'], sonar_server=sonar_paramters['API_DOMAIN'])
        result = []
        for page_items in sonar.get_rules():
            for rule in page_items:
                lang_obj = get_lang_by_key(rule['lang'])
                r_s = get_tactic_type_scope(get_issue_type_by_sonar(rule['type']))
                r_r = get_tactic_risk_scope(get_risk_by_severity(rule['severity']))
                r_t = 0
                # （类型权重+风险因素）* (标签系数*N) + （类型权重+风险因素）
                risk_scope = (r_s + r_r) * r_t + (r_s + r_r)
                rule_obj = TacticInfo(
                    lang=lang_obj,
                    engine=sonar_engine,
                    is_active=True,
                    key=rule['key'],
                    name=rule['name'],
                    description=md(rule['htmlDesc']),
                    type=get_issue_type_by_sonar(rule['type']),
                    risk=get_risk_by_severity(rule['severity']),
                    nature_type=2,
                    attribution_type=1,
                    revision=0.01,
                    risk_scope=risk_scope,
                )
                result.append(rule_obj)
                if len(result) % 200 == 0:
                    try:
                        TacticInfo.objects.bulk_create(result)
                    except:
                        pass
                    finally:
                        result = []
        if result:
            try:
                TacticInfo.objects.bulk_create(result)
            except:
                pass

