# coding: utf-8
from __future__ import unicode_literals

from django.core.cache import cache

from seecode.libs.core.data import logger
from seecode.apps.tactic.models import EngineInfo
from seecode.apps.tactic.models import TacticInfo
from seecode.libs.units import close_old_connections
from seecode.libs.core.exceptions import QueryConditionIsEmptyException
from seecode.libs.dal.upgrade_version import update_client_major_version
from seecode.libs.dal.upgrade_version import update_client_revision_version
from seecode.libs.core.cache_key import CONFIG_ENGINE_CACHE


def registration_engine():
    update_client_major_version()
    pass


def get_all_engine():
    """

    :return:
    """
    cache_obj = cache.get(CONFIG_ENGINE_CACHE[2])
    if cache_obj:
        return cache_obj

    close_old_connections()
    result = EngineInfo.objects.all()
    cache.set(CONFIG_ENGINE_CACHE[2], result, CONFIG_ENGINE_CACHE[0])
    return result


def get_all_customize_engine():
    """

    :return:
    """
    cache_obj = cache.get(CONFIG_ENGINE_CACHE[3])
    if cache_obj:
        return cache_obj

    close_old_connections()
    result = EngineInfo.objects.filter(is_customize=True)
    cache.set(CONFIG_ENGINE_CACHE[3], result, CONFIG_ENGINE_CACHE[0])
    return result


def update_engine_obj(**kwargs):
    """
    :param kwargs:
    :return:
    """
    description = kwargs.get('description', '')
    key_list = kwargs.get('key_list', [])
    value_list = kwargs.get('value_list', [])
    engine_id = kwargs.get('engine_id', None)
    
    try:
        engine_obj = EngineInfo.objects.filter(id=engine_id).first()
        if engine_obj:
            parameters = {}
            for index in range(0, len(key_list)):
                parameters[key_list[index]] = value_list[index]
            engine_obj.description = description.strip()
            engine_obj.config = str(parameters)
            engine_obj.revision = round(engine_obj.revision + 0.1, 2)
            engine_obj.whitelist_count = TacticInfo.objects.filter(engine__id=engine_id, nature_type=1).count()
            engine_obj.blacklist_count = TacticInfo.objects.filter(engine__id=engine_id, nature_type=2).count()

            engine_obj.save()
            cache.set('{0}:{1}'.format(CONFIG_ENGINE_CACHE[1], engine_id), None, 0)
            update_client_revision_version(
                action=3,
                module=1,
                description="修改“{0}”扫描引擎配置".format(engine_obj.name)
            )
            return True
        return False
    except Exception as ex:
        import traceback;traceback.print_exc()
        return False


def _get_engine_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    result = None
    engine_id = kwargs.get('engine_id', None)
    module_name = kwargs.get('module_name', None)
    close_old_connections()

    try:
        sql_where = {}
        if engine_id:
            sql_where['id'] = int(engine_id)
        if module_name:
            sql_where['module_name'] = module_name
        if not sql_where:
            raise QueryConditionIsEmptyException(u'Missing "engine_id" key parameters!')

        item = EngineInfo.objects.get(**sql_where)
        result = item
    except EngineInfo.DoesNotExist as ex:
        logger.warning(ex)
    return result


def get_engine_by_id(engine_id):
    """

    :param engine_id:
    :return:
    """
    cache_key = '{0}:{1}'.format(CONFIG_ENGINE_CACHE[1], engine_id)
    cache_obj = cache.get(cache_key)
    if cache_obj:
        return cache_obj
    obj = _get_engine_obj(engine_id=engine_id)
    if obj:
        cache.set(cache_key, obj, CONFIG_ENGINE_CACHE[0])
    return obj


def get_engine_by_module_name(module_name):
    """

    :param module_name:
    :return:
    """

    cache_key = '{0}:{1}'.format(CONFIG_ENGINE_CACHE[1], module_name)
    cache_obj = cache.get(cache_key)
    if cache_obj:
        return cache_obj
    obj = _get_engine_obj(module_name=module_name)
    if obj:
        cache.set(cache_key, obj, CONFIG_ENGINE_CACHE[0])
    return obj


def get_engine_by_scanner_id(scanner_id):
    """

    :param scanner_id:
    :return:
    """
    if scanner_id == 1:
        module_name = 'seecode_scanner.lib.engines.sonarscanner'
    elif scanner_id == 2:
        module_name = 'seecode_scanner.lib.engines.rulescanner'
    else:
        module_name = 'seecode_scanner.lib.engines.pluginscanner'

    return get_engine_by_module_name(module_name)
