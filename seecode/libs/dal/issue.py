# coding: utf-8
from __future__ import unicode_literals

from django.core.cache import cache

from seecode.apps.scan.models import IssueInfo
from seecode.libs.core.cache_key import ISSUE_CACHE
from seecode.libs.core.cache_key import PROJECT_APP_CACHE
from seecode.libs.core.common import get_risk_name
from seecode.libs.core.common import get_risk_key
from seecode.libs.core.data import logger
from seecode.libs.core.exceptions import ParameterIsEmptyException
from seecode.libs.core.exceptions import QueryConditionIsEmptyException
from seecode.libs.dal.tactic import get_tactic_by_key
from seecode.libs.dal.config import get_config
from seecode.libs.dal.dependent import get_dependent_by_name
from seecode.libs.units import close_old_connections


def create_issue_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    tactic_obj = kwargs.get('tactic_obj', None)
    app_obj = kwargs.get('app_obj', None)
    title = kwargs.get('title', None)
    file_name = kwargs.get('file_name', None)
    report_detail_url = kwargs.get('report_detail_url', None)
    last_commit = kwargs.get('last_commit', '')
    last_commit_author = kwargs.get('last_commit_author', '')
    last_commit_author_email = kwargs.get('last_commit_author_email', '')
    start_line = kwargs.get('start_line', '')
    end_line = kwargs.get('end_line', '')
    code_segment = kwargs.get('code_segment', '')
    evidence_content = kwargs.get('evidence_content', '')
    is_false_positive = kwargs.get('is_false_positive', False)
    whitelist_rule_id = kwargs.get('whitelist_rule_id', None)
    status = kwargs.get('status', 1)

    if not all((tactic_obj, app_obj, title, file_name)):
        raise ParameterIsEmptyException('"tactic_obj, app_obj, title, file_name" parameters cannot be empty.')

    if title and len(title) > 500:
        title = title[:500]

    if is_false_positive:
        is_false_positive = True

    if status:
        status = int(status)

    if start_line:
        start_line = int(start_line)

    if end_line:
        end_line = int(end_line)

    close_old_connections()

    issue = IssueInfo(
        tactic=tactic_obj,
        app=app_obj,
        title=title,
        file_name=file_name,
        report_detail_url=report_detail_url,
        last_commit=last_commit,
        last_commit_author=last_commit_author,
        last_commit_author_email=last_commit_author_email,
        start_line=start_line,
        end_line=end_line,
        code_segment=code_segment,
        evidence_content=evidence_content,
        is_false_positive=is_false_positive,
        status=status,
    )

    if is_false_positive:
        issue.whitelist_rule_id = whitelist_rule_id
    issue.save()

    if issue:
        # TODO gitlab/jira submit issue
        pass
    return issue


def _get_issue_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    result = None
    issue_id = kwargs.get('issue_id', None)
    close_old_connections()

    try:
        sql_where = {}
        if issue_id:
            sql_where['id'] = int(issue_id)
        if not sql_where:
            raise QueryConditionIsEmptyException(u'Missing "issue_id" key parameters!')

        item = IssueInfo.objects.get(**sql_where)
        result = item
    except IssueInfo.DoesNotExist as ex:
        logger.warning(ex)
    return result


def get_issue_by_info(tactic_id, app_id, file_name, start_line):
    """

    :param tactic_id:
    :param app_id:
    :param file_name:
    :param start_line:
    :return:
    """
    result = None

    close_old_connections()

    try:
        sql_where = {}
        if tactic_id:
            sql_where['tactic__id'] = int(tactic_id)
        if app_id:
            sql_where['app__id'] = int(app_id)
        if file_name:
            sql_where['file_name'] = file_name.strip()
        if start_line:
            sql_where['start_line'] = int(start_line)

        if not sql_where:
            raise QueryConditionIsEmptyException(u'Missing "tactic_id, app_id, file_name, start_line" key parameters!')

        result = IssueInfo.objects.filter(**sql_where).first()
    except IssueInfo.DoesNotExist as ex:
        import traceback;
        traceback.print_exc()  # FIXME log
    return result


def update_issue_obj(**kwargs):
    """

    :param kwargs:
    :return:
    """
    result = None
    issue_id = kwargs.get('issue_id', None)
    title = kwargs.get('title', None)
    user = kwargs.get('user', None)
    comment = kwargs.get('comment', None)
    is_whitelist = kwargs.get('is_whitelist', False)
    code_segment = kwargs.get('code_segment', None)
    is_false_positive = kwargs.get('is_false_positive', False)
    last_commit_author = kwargs.get('last_commit_author', '')
    last_commit_author_email = kwargs.get('last_commit_author_email', '')
    status = kwargs.get('status', None)

    try:
        sql_where = {}
        if issue_id:
            sql_where['id'] = int(issue_id)
        if not sql_where:
            raise QueryConditionIsEmptyException(u'Missing "issue_id" key parameters!')

        result = IssueInfo.objects.filter(**sql_where).first()
        if result:
            # app 风险数量减少
            if status and int(status) in (2, 3, 5) and int(status) != result.status and result.tactic.type == 3:
                risk = result.tactic.risk
                if risk == 1 and result.app.critical > 0:
                    result.app.critical -= 1
                elif risk == 2 and result.app.high > 0:
                    result.app.high -= 1
                elif risk == 3 and result.app.medium > 0:
                    result.app.medium -= 1
                elif risk == 4 and result.app.low > 0:
                    result.app.low -= 1
                elif risk == 5 and result.app.info > 0:
                    result.app.info -= 1
                # 从新计分数
                result.app.save()

            if code_segment:
                result.code_segment = code_segment
            if status:
                result.status = int(status)
            if title:
                result.title = title.strip()
            if is_whitelist:
                result.is_whitelist = True
            if is_false_positive:
                result.is_false_positive = True
            if last_commit_author and not result.last_commit_author:
                result.last_commit_author = last_commit_author
                result.last_commit_author_email = last_commit_author_email
            result.save(
                comment=comment,
                status=status,
                user=user
            )
            cache.set('{0}:{1}'.format(PROJECT_APP_CACHE[1], result.app.id), None, 0)
            cache.set('{0}:{1}'.format(PROJECT_APP_CACHE[4], result.app.id), None, 0)
            cache.set('{0}:{1}'.format(ISSUE_CACHE[1], result.id), None, 0)
            # TODO update sonarqube issue
    except IssueInfo.DoesNotExist as ex:
        pass  # FIXME log
    return result


def get_issue_by_id(issue_id):
    """

    :param issue_id:
    :return:
    """
    cache_key = '{0}:{1}'.format(ISSUE_CACHE[1], issue_id)
    cache_obj = cache.get(cache_key)
    if cache_obj:
        return cache_obj
    obj = _get_issue_obj(issue_id=issue_id)
    if obj:
        cache.set(cache_key, obj, ISSUE_CACHE[0])
    return obj


def create_or_update(**kwargs):
    """

    :param kwargs:
    :return:
    """
    app_obj = kwargs.get('app_obj')
    file_name = kwargs.get('file_name')
    start_line = kwargs.get('start_line')
    rule_key = kwargs.get('rule_key')
    kwargs['tactic_obj'] = get_tactic_by_key(key=rule_key)
    if kwargs['tactic_obj']:
        kwargs['title'] = kwargs['tactic_obj'].name

    issue_obj = get_issue_by_info(kwargs['tactic_obj'].id, app_obj.id, file_name, start_line)
    if issue_obj:
        kwargs['issue_id'] = issue_obj.id
        return update_issue_obj(**kwargs)
    else:
        return create_issue_obj(**kwargs)

