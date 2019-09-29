# coding: utf-8
from __future__ import unicode_literals
import datetime

from seecode.apps.node.models import UpgradeChangelogInfo
from seecode.libs.core.exceptions import ParameterIsEmptyException
from seecode.libs.core.exceptions import QueryConditionIsEmptyException
from seecode.libs.units import close_old_connections


def create_changelog_obj(**kwargs):
    """
    插入历史
    :return:
    """
    action = kwargs.get('action', None)
    module = kwargs.get('module', None)
    description = kwargs.get('description', '')

    if not all((action, module, description,)):
        raise ParameterIsEmptyException(u'"action, module, description" parameters cannot be empty !')

    close_old_connections()
    changelog = UpgradeChangelogInfo.objects.filter(action=action, module=module, description=description).first()

    if not changelog:
        changelog = UpgradeChangelogInfo(
            action=action,
            module=module,
            description=description,
        )
    changelog.save()
    return changelog


def release_version(version):
    """
    发布版本
    :return:
    """
    result = False
    if version:
        UpgradeChangelogInfo.objects.filter(is_archive=False).update(is_archive=True, version=version)
        result = True
    return result


def get_changelog():
    """

    (1, u"扫描引擎"),
    (2, u"策略规则"),
    (3, u"扫描模板"),
    :return:
    """
    result = {
        'features': {
            u'1': [],
            u'2': [],
            u'3': [],
        },
        'bugfix': {
            u'1': [],
            u'2': [],
            u'3': [],
        }
    }
    changelog_list = UpgradeChangelogInfo.objects.filter(is_archive=False)
    for item in changelog_list:
        if item.action in (1, 2):
            if item.module == 1:
                result['features']['1'].append(item.description)
            elif item.module == 2:
                result['features']['2'].append(item.description)
            elif item.module == 3:
                result['features']['3'].append(item.description)
        else:
            if item.module == 1:
                result['bugfix']['1'].append(item.description)
            elif item.module == 2:
                result['bugfix']['2'].append(item.description)
            elif item.module == 3:
                result['bugfix']['3'].append(item.description)

    return result


def make_changelog_markdown(changelog, ver_no):
    """

    :param changelog:
    :param ver_no:
    :return:
    """
    result = []
    result.append('## v{0}({1})'.format(ver_no, datetime.datetime.now().strftime("%Y-%m-%d")))
    count = 1
    for section, contents in changelog.items():
        result.append('\n\n---\n\n### {0}. {1}\n\n'.format(count, section.upper()))
        sub_count = 1
        for module_id, bugs in contents.items():
            if module_id == '1':
                title = "扫描引擎"
            elif module_id == '2':
                title = "策略规则"
            elif module_id == '3':
                title = '扫描模板'
            else:
                title = '其他'
            if bugs:
                result.append('\n#### {0}.{1}. {2}\n\n'.format(count, sub_count, title))
                for bug in bugs:
                    bug_list = bug.split('\n')
                    for _ in bug_list:
                        result.append('* {0}\n'.format(_))
                sub_count += 1
        count += 1
    return ''.join(result)
