# coding: utf-8
from __future__ import unicode_literals

import ast
import os

from lxml import etree as ET
from django.core.cache import cache
from django.conf import settings

from seecode.apps.scan.models import ScanProfileInfo
from seecode.libs.core.log import logger
from seecode.libs.core.enum import TACTIC_TYPE
from seecode.libs.units import close_old_connections
from seecode.libs.core.exceptions import ParameterIsEmptyException
from seecode.libs.core.exceptions import QueryConditionIsEmptyException
from seecode.libs.units import parse_int
from seecode.libs.units import parse_bool
from seecode.libs.core.common import make_dir
from seecode.libs.core.common import get_risk_name
from seecode.libs.core.common import get_tactic_type
from seecode.libs.dal.upgrade_version import update_client_minor_version
from seecode.libs.dal.upgrade_version import update_client_revision_version
from seecode.libs.core.cache_key import SCAN_PROFILE_CACHE


def create_profile_obj(**kwargs):
    """
    :param kwargs:
    :return:
    """
    host_obj = kwargs.get('host_obj', None)
    name = kwargs.get('name', None)
    description = kwargs.get('description', '')
    exclude_dir = kwargs.get('exclude_dir', '')
    exclude_ext = kwargs.get('exclude_ext', '')
    exclude_file = kwargs.get('exclude_file', '')
    exclude_java_package = kwargs.get('exclude_java_package', '')
    config = kwargs.get('config', '')
    enable_commit_issue = parse_bool(kwargs.get('enable_commit_issue', False))
    enable_auto_ignore = parse_bool(kwargs.get('enable_auto_ignore', False))
    task_timeout = parse_int(kwargs.get('task_timeout', 60*60*2))

    if not all((name, )):
        raise ParameterIsEmptyException(u'"name" parameters cannot be empty !')

    if name and len(name) > 32:
        name = name[:32]

    close_old_connections()

    profile = ScanProfileInfo(
        host=host_obj,
        name=name,
        description=description,
        exclude_dir=exclude_dir,
        exclude_ext=exclude_ext,
        exclude_file=exclude_file,
        exclude_java_package=exclude_java_package,
        config=config,
        enable_commit_issue=enable_commit_issue,
        enable_auto_ignore=enable_auto_ignore,
        task_timeout=task_timeout,
    )
    profile.save()
    update_client_minor_version(
        action=1,
        module=3,
        description='添加“{0}”扫描模板'.format(name)
    )

    return profile


def _get_profile_obj(**kwargs):
    """
    获取资产
    :param kwargs:
    :return:
    """
    profile_id = kwargs.get('profile_id', None)
    name = kwargs.get('name', None)
    close_old_connections()

    try:
        sql_where = {}
        if profile_id:
            sql_where['id'] = int(profile_id)
        if name:
            sql_where['name'] = name
        if not sql_where:
            raise QueryConditionIsEmptyException(u'Missing "profile_id, name" key parameters!')
        item = ScanProfileInfo.objects.get(**sql_where)
        return item
    except ScanProfileInfo.DoesNotExist as ex:
        logger.warn(ex)
        return None


def update_profile_obj(**kwargs):
    """
    获取资产
    :param kwargs:
    :return:
    """
    profile_id = kwargs.get('profile_id', None)
    host_obj = kwargs.get('host_obj', None)
    name = kwargs.get('name', None)
    description = kwargs.get('description', '')
    exclude_dir = kwargs.get('exclude_dir', '')
    exclude_ext = kwargs.get('exclude_ext', '')
    exclude_file = kwargs.get('exclude_file', '')
    exclude_java_package = kwargs.get('exclude_java_package', '')
    config = kwargs.get('config', None)
    enable_commit_issue = parse_bool(kwargs.get('enable_commit_issue', None))
    enable_auto_ignore = parse_bool(kwargs.get('enable_auto_ignore', None))
    task_timeout = parse_int(kwargs.get('task_timeout', 60 * 60 * 2))

    try:
        sql_where = {}

        if profile_id:
            sql_where['id'] = int(profile_id)
        if not sql_where:
            raise QueryConditionIsEmptyException(u'Missing "profile_id" key parameters!')

        item = ScanProfileInfo.objects.get(**sql_where)
        if item:
            item.enable_commit_issue = enable_commit_issue
            item.enable_auto_ignore = enable_auto_ignore
            if host_obj:
                item.host = host_obj
            if name:
                item.name = name
            item.description = description
            item.exclude_dir = exclude_dir
            item.exclude_ext = exclude_ext
            item.exclude_file = exclude_file
            item.exclude_java_package = exclude_java_package
            item.task_timeout = task_timeout
            if config:
                item.config = config
            item.revision = round(item.revision + 0.1, 2)
            cache.set('{0}:{1}'.format(SCAN_PROFILE_CACHE[1], item.id), None, 0)
            cache.set('{0}:{1}'.format(SCAN_PROFILE_CACHE[2], item.id), None, 0)
            cache.set('{0}:{1}'.format(SCAN_PROFILE_CACHE[3], item.id), None, 0)
            cache.set('{0}:{1}'.format(SCAN_PROFILE_CACHE[4], item.id), None, 0)
            cache.set('{0}'.format(SCAN_PROFILE_CACHE[5]), None, 0)
            update_client_revision_version(
                action=3,
                module=3,
                description='修改“{0}”扫描模板内容'.format(item.name)
            )
            item.save()
        return item
    except ScanProfileInfo.DoesNotExist as ex:
        logger.warn(ex)
        return None


def get_profile_by_id(profile_id):
    """

    :param profile_id:
    :return:
    """
    cache_key = '{0}:{1}'.format(SCAN_PROFILE_CACHE[1], profile_id)
    cache_obj = cache.get(cache_key)
    if cache_obj:
        return cache_obj
    obj = _get_profile_obj(profile_id=profile_id)
    if obj:
        cache.set(cache_key, obj, SCAN_PROFILE_CACHE[0])
    return obj


def get_profile_default():
    """
    :return:
    """
    return get_profile_by_id(profile_id=1)


def get_profile_by_name(name):
    """

    :param name:
    :return:
    """
    return _get_profile_obj(name=name)


def get_profile_all():
    """

    :return:
    """
    cache_obj = cache.get(SCAN_PROFILE_CACHE[5])
    if cache_obj:
        return cache_obj
    obj = ScanProfileInfo.objects.all()
    if obj:
        cache.set(SCAN_PROFILE_CACHE[5], obj, SCAN_PROFILE_CACHE[0])
    return obj


def get_profile_engines_by_id(profile_id):
    """

    :param profile_id:
    :return:
    """
    engines = []
    if profile_id:
        cache_key = '{0}:{1}'.format(SCAN_PROFILE_CACHE[2], profile_id)
        cache_obj = cache.get(cache_key)
        if cache_obj:
            engines = cache_obj
        else:
            obj = _get_profile_obj(profile_id=profile_id)
            if obj:
                engines = obj.engines.all()
                cache.set(cache_key, engines, SCAN_PROFILE_CACHE[0])
    return engines


def get_profile_rule_by_id(profile_id):
    """

    :param profile_id:
    :return:
    """
    cache_key = '{0}:{1}'.format(SCAN_PROFILE_CACHE[3], profile_id)
    cache_obj = cache.get(cache_key)
    if cache_obj:
        return cache_obj
    obj = _get_profile_obj(profile_id=profile_id)
    rules = []
    if obj:
        rules = obj.rules.all()
        cache.set(cache_key, rules, SCAN_PROFILE_CACHE[0])
    return rules


def get_profile_plugin_by_id(profile_id):
    """

    :param profile_id:
    :return:
    """
    cache_key = '{0}:{1}'.format(SCAN_PROFILE_CACHE[4], profile_id)
    cache_obj = cache.get(cache_key)
    if cache_obj:
        return cache_obj
    obj = _get_profile_obj(profile_id=profile_id)
    plugins = []
    if obj:
        plugins = obj.plugins.all()
        cache.set(cache_key, plugins, SCAN_PROFILE_CACHE[0])
    return plugins


def clean_engine_cache(profile_id):
    """

    :param profile_id:
    :return:
    """
    cache.set('{0}:{1}'.format(SCAN_PROFILE_CACHE[3], profile_id), None, 0)
    cache.set('{0}:{1}'.format(SCAN_PROFILE_CACHE[4], profile_id), None, 0)


def delete_profile(profile_id):
    """
    :param profile_id:
    :return:
    """
    cache_key = '{0}:{1}'.format(SCAN_PROFILE_CACHE[2], profile_id)
    cache.set(cache_key, None, 0)
    obj = ScanProfileInfo.objects.filter(id=profile_id).first()
    update_client_minor_version(
        action=2,
        module=3,
        description='删除“{0}”扫描模板'.format(obj.name)
    )
    obj.delete()


def dump_scan_template(profile_id, dump_path=None):
    """

    :param profile_id:
    :param dump_path:
    :return:
    """
    template_style_version = '1.0.0'
    if not dump_path:
        dump_path = '{0}'.format(settings.UPGRADE_ROOT)
    dump_plugin_whitelist = os.path.join(dump_path, 'plugins', 'whitelist')
    dump_plugin_blacklist = os.path.join(dump_path, 'plugins', 'blacklist')
    make_dir([dump_path, dump_plugin_whitelist, dump_plugin_blacklist])

    if profile_id:
        profile = get_profile_by_id(profile_id)
        if profile.config:
            profile_config = ast.literal_eval(profile.config)
        else:
            profile_config = None
        data = ET.Element('template')
        data.set('version', template_style_version)
        conf = ET.SubElement(data, 'config')
        conf.set('sync', 'True')
        conf.set('enable', 'True')
        name = ET.SubElement(conf, 'name')
        name.text = profile.name
        version = ET.SubElement(conf, 'version')
        version.text = str(profile.revision)
        exclude_dir = ET.SubElement(conf, 'exclude_dir')
        exclude_dir.text = profile.exclude_dir
        exclude_ext = ET.SubElement(conf, 'exclude_ext')
        exclude_ext.text = profile.exclude_ext
        exclude_file = ET.SubElement(conf, 'exclude_file')
        exclude_file.text = profile.exclude_file
        task_timeout = ET.SubElement(conf, 'task_timeout')
        task_timeout.text = str(profile.task_timeout)
        engines = ET.SubElement(data, 'engines')

        for engine in profile.engines.all():
            engine_node = ET.SubElement(engines, 'engine')
            engine_node.set('name', engine.name)
            # parameters
            parameters = ET.SubElement(engine_node, 'parameters')
            engine_config = ast.literal_eval(engine.config)
            for k, v in engine_config.items():
                item = ET.SubElement(parameters, 'item')
                item.set("name", k)
                item.text = str(v)
            if profile_config and engine.module_name in profile_config:
                for k1, v2 in profile_config[engine.module_name].items():
                    item = ET.SubElement(parameters, 'item')
                    item.set("name", k1)
                    item.text = str(v2)
            # rule
            if engine.module_name == 'seecode_scanner.lib.engines.rulescanner':
                component = ET.SubElement(engine_node, 'component')
                # component
                for item in profile.tactics.filter(rule_match_type=4, engine__id=engine.id):
                    item_node = ET.SubElement(component, 'item')
                    item_node.set("id", str(item.id))
                    item_node_name = ET.SubElement(item_node, 'name')
                    item_node_name.text = item.name
                    item_node_key = ET.SubElement(item_node, 'key')
                    item_node_key.text = item.key
                    item_node_revision = ET.SubElement(item_node, 'revision')
                    item_node_revision.text = str(item.revision)
                    item_node_risk = ET.SubElement(item_node, 'risk')
                    item_node_risk.set("id", str(item.risk))
                    item_node_risk.text = get_risk_name(item.risk)
                    item_node_category = ET.SubElement(item_node, 'category')
                    item_node_category.text = get_tactic_type(item.type)
                    item_node_match_type = ET.SubElement(item_node, 'match_type')
                    if item.rule_value == '1':
                        item_node_match_type.text = 'groupId'
                    else:
                        item_node_match_type.text = 'name'
                    item_node_match_content = ET.SubElement(item_node, 'match_content')
                    item_node_match_content.text = ET.CDATA(item.component_name)
                    item_node_match_regex = ET.SubElement(item_node, 'match_regex')
                    item_node_match_regex.text = ET.CDATA(str(item.rule_regex))
                    item_node_match_regex.set("flag", item.rule_regex_flag)

                # whitelist
                whitelist = ET.SubElement(engine_node, 'whitelist')
                for item in profile.tactics.filter(nature_type=1, attribution_type=1, engine__id=engine.id).exclude(rule_match_type=4):
                    item_node = ET.SubElement(whitelist, 'item')
                    item_node.set("id", str(item.id))
                    item_node_name = ET.SubElement(item_node, 'name')
                    item_node_name.text = item.name
                    item_node_key = ET.SubElement(item_node, 'key')
                    item_node_key.text = item.key
                    item_node_revision = ET.SubElement(item_node, 'revision')
                    item_node_revision.text = str(item.revision)
                    item_node_risk = ET.SubElement(item_node, 'risk')
                    item_node_risk.set("id", str(item.risk))
                    item_node_risk.text = get_risk_name(item.risk)
                    item_node_category = ET.SubElement(item_node, 'category')
                    item_node_category.text = get_tactic_type(item.type)
                    item_node_category.set("id", str(item.type))

                    item_node_match_type = ET.SubElement(item_node, 'match_type')
                    if item.rule_match_type == 1:
                        item_node_match_type.text = 'dir'
                    elif item.rule_match_type == 2:
                        item_node_match_type.text = 'file'
                    elif item.rule_match_type == 3:
                        item_node_match_type.text = 'content'
                        item_node_match_ext = ET.SubElement(item_node, 'match_ext')
                        item_node_match_ext.text = item.rule_value

                    item_node_match_regex = ET.SubElement(item_node, 'match_regex')
                    item_node_match_regex.text = str(item.rule_regex)
                    item_node_match_regex.set("flag", item.rule_regex_flag)

                # blacklist
                blacklist = ET.SubElement(engine_node, 'blacklist')
                for item in profile.tactics.filter(nature_type=2, attribution_type=1, engine__id=engine.id).exclude(rule_match_type=4):
                    item_node = ET.SubElement(blacklist, 'item')
                    item_node.set("id", str(item.id))
                    item_node_name = ET.SubElement(item_node, 'name')
                    item_node_name.text = item.name
                    item_node_key = ET.SubElement(item_node, 'key')
                    item_node_key.text = item.key
                    item_node_revision = ET.SubElement(item_node, 'revision')
                    item_node_revision.text = str(item.revision)
                    item_node_risk = ET.SubElement(item_node, 'risk')
                    item_node_risk.set("id", str(item.risk))
                    item_node_risk.text = get_risk_name(item.risk)
                    item_node_category = ET.SubElement(item_node, 'category')
                    item_node_category.text = get_tactic_type(item.type)
                    item_node_category.set("id", str(item.type))

                    item_node_match_type = ET.SubElement(item_node, 'match_type')
                    if item.rule_match_type == 1:
                        item_node_match_type.text = 'dir'
                    elif item.rule_match_type == 2:
                        item_node_match_type.text = 'file'
                    elif item.rule_match_type == 3:
                        item_node_match_type.text = 'content'
                        item_node_match_ext = ET.SubElement(item_node, 'match_ext')
                        item_node_match_ext.text = item.rule_value

                    item_node_match_regex = ET.SubElement(item_node, 'match_regex')
                    item_node_match_regex.text = str(item.rule_regex)
                    item_node_match_regex.set("flag", item.rule_regex_flag)

            # plugin
            if engine.module_name == 'seecode_scanner.lib.engines.pluginscanner':
                # whitelist
                whitelist = ET.SubElement(engine_node, 'whitelist')
                for item in profile.tactics.filter(nature_type=1, attribution_type=2, engine__id=engine.id):
                    item_node = ET.SubElement(whitelist, 'item')
                    item_node.set("id", str(item.id))
                    item_node_name = ET.SubElement(item_node, 'name')
                    item_node_name.text = item.name
                    item_node_key = ET.SubElement(item_node, 'key')
                    item_node_key.text = item.key
                    item_node_revision = ET.SubElement(item_node, 'revision')
                    item_node_revision.text = str(item.revision)
                    item_node_risk = ET.SubElement(item_node, 'risk')
                    item_node_risk.set("id", str(item.risk))
                    item_node_risk.text = get_risk_name(item.risk)
                    item_node_category = ET.SubElement(item_node, 'category')
                    item_node_category.text = get_tactic_type(item.type)
                    item_node_category.set("id", str(item.type))
                    item_node_module = ET.SubElement(item_node, 'module')
                    item_node_module.text = item.plugin_module_name
                    item_node_script = ET.SubElement(item_node, 'script')
                    item_node_script.text = 'plugins/whitelist/{0}.py'.format(item.plugin_name)
                    with open(os.path.join(dump_plugin_whitelist, '{0}.py'.format(item.plugin_name)), 'w') as fp:
                        fp.write(item.plugin_content)
                # blacklist
                blacklist = ET.SubElement(engine_node, 'blacklist')
                for item in profile.tactics.filter(nature_type=2, attribution_type=2, engine__id=engine.id):
                    item_node = ET.SubElement(blacklist, 'item')
                    item_node.set("id", str(item.id))
                    item_node_name = ET.SubElement(item_node, 'name')
                    item_node_name.text = item.name
                    item_node_key = ET.SubElement(item_node, 'key')
                    item_node_key.text = item.key
                    item_node_revision = ET.SubElement(item_node, 'revision')
                    item_node_revision.text = str(item.revision)
                    item_node_risk = ET.SubElement(item_node, 'risk')
                    item_node_risk.set("id", str(item.risk))
                    item_node_risk.text = get_risk_name(item.risk)
                    item_node_category = ET.SubElement(item_node, 'category')
                    item_node_category.text = get_tactic_type(item.type)
                    item_node_category.set("id", str(item.type))
                    item_node_module = ET.SubElement(item_node, 'module')
                    item_node_module.text = item.plugin_module_name
                    item_node_script = ET.SubElement(item_node, 'script')
                    item_node_script.text = 'plugins/blacklist/{0}.py'.format(item.plugin_name)
                    with open(os.path.join(dump_plugin_blacklist, '{0}.py'.format(item.plugin_name)), 'w') as fp:
                        fp.write(item.plugin_content)

        mydata = ET.tostring(data, encoding='utf-8')
        file_name = os.path.join(dump_path, '{0}.xml'.format(profile.name))
        with open(file_name, "wb") as fp:
            fp.write(b"<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n")
            fp.write(mydata)
