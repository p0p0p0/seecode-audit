# coding: utf-8
from __future__ import unicode_literals

from django.core.cache import cache

from seecode.libs.core.data import logger
from seecode.apps.tactic.models import VulnInfo
from seecode.libs.units import close_old_connections
from seecode.libs.core.exceptions import ParameterIsEmptyException
from seecode.libs.core.exceptions import QueryConditionIsEmptyException
from seecode.libs.core.cache_key import VULN_CACHE


def create_vuln_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    cate_obj = kwargs.get('cate_obj', None)
    title = kwargs.get('title', None)
    description = kwargs.get('description', '')
    solution = kwargs.get('solution', '')
    reference = kwargs.get('reference', '')
    risk = kwargs.get('risk', None)
    hit = kwargs.get('hit', 0)
    impact_version = kwargs.get('impact_version', '')
    cnnvd = kwargs.get('cnnvd', '')
    cnvd = kwargs.get('cnvd', '')
    cve = kwargs.get('cve', '')
    bugtraq = kwargs.get('bugtraq', False)
    origin = kwargs.get('origin', None)
    find_time = kwargs.get('find_time', None)

    if not all((cate_obj, title, risk, )):
        raise ParameterIsEmptyException(u'"cate_obj, title, risk" parameters cannot be empty !')

    if title and len(title)>255:
        title = title[:255]

    if risk:
        risk = int(risk)

    close_old_connections()

    vuln = VulnInfo(
        cate=cate_obj,
        title=title,
        description=description,
        solution=solution,
        reference=reference,
        risk=risk,
        hit=hit,
        impact_version=impact_version,
        cnnvd=cnnvd,
        cnvd=cnvd,
        cve=cve,
        bugtraq=bugtraq,
        origin=origin,
        find_time=find_time
    )
    vuln.save()
    return vuln


def _get_vuln_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    result = None
    vuln_id = kwargs.get('vuln_id', None)
    title = kwargs.get('title', None)
    cve = kwargs.get('cve', None)
    close_old_connections()

    try:
        sql_where = {}
        if vuln_id:
            sql_where['id'] = int(vuln_id)
        if title:
            sql_where['title'] = title.strip()
        if cve:
            sql_where['cve'] = cve.strip()

        if not sql_where:
            raise QueryConditionIsEmptyException(u'Missing "vuln_id, title" key parameters!')

        item = VulnInfo.objects.get(**sql_where)
        result = item
    except VulnInfo.DoesNotExist as ex:
        logger.warning(ex)
    return result


def update_vuln_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    result = None
    vuln_id = kwargs.get('vuln_id', None)
    cate_obj = kwargs.get('cate_obj', None)
    title = kwargs.get('title', None)
    description = kwargs.get('description', '')
    solution = kwargs.get('solution', '')
    reference = kwargs.get('reference', '')
    risk = kwargs.get('risk', None)
    hit = kwargs.get('hit', 0)
    impact_version = kwargs.get('impact_version', '')
    cnnvd = kwargs.get('cnnvd', '')
    cnvd = kwargs.get('cnvd', '')
    cve = kwargs.get('cve', '')
    bugtraq = kwargs.get('bugtraq', False)
    origin = kwargs.get('origin', None)
    find_time = kwargs.get('find_time', None)

    try:
        sql_where = {}

        if vuln_id:
            sql_where['id'] = int(vuln_id)

        if not sql_where:
            raise  QueryConditionIsEmptyException(u'Missing "vuln_id" key parameters!')

        item = VulnInfo.objects.get(**sql_where)
        if item:
            if cate_obj:
                item.cate = cate_obj
            if title:
                item.title = title
            item.description = description
            item.solution = solution
            if reference:
                item.reference = reference.strip()
            item.risk = int(risk)
            item.hit = int(hit)
            item.impact_version = impact_version
            item.cnnvd = cnnvd
            item.cnvd = cnvd
            item.cve = cve
            item.bugtraq = bugtraq
            if origin:
                item.origin = origin
            if find_time:
                item.find_time = find_time.strip()

            item.save()
            cache.set('{0}:{1}'.format(VULN_CACHE[1], item.id), None, 0)
            cache.set('{0}:{1}'.format(VULN_CACHE[2], item.cve), None, 0)
            result = item
    except VulnInfo.DoesNotExist as ex:
        logger.warning(ex)
    return result


def get_vuln_by_id(vuln_id):
    """

    :param vuln_id:
    :return:
    """
    if vuln_id:
        cache_key = '{0}:{1}'.format(VULN_CACHE[1], vuln_id)
        cache_obj = cache.get(cache_key)
        if cache_obj:
            return cache_obj
    obj = _get_vuln_obj(vuln_id=vuln_id)
    if obj:
        cache.set(cache_key, obj, VULN_CACHE[0])
    return obj


def get_vuln_by_cve(cve):
    """

    :param cve:
    :return:
    """
    if cve:
        cache_key = '{0}:{1}'.format(VULN_CACHE[2], cve)
        cache_obj = cache.get(cache_key)
        if cache_obj:
            return cache_obj
    obj = _get_vuln_obj(cve=cve)
    if obj:
        cache.set(cache_key, obj, VULN_CACHE[0])
    return obj


def get_vuln_by_title(title):
    """

    :param title:
    :return:
    """
    return _get_vuln_obj(title=title)
