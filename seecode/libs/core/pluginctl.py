# coding: utf-8

import os

from django.conf import settings

PLUGIN_PATH = os.path.join(settings.BASE_DIR, 'libs', 'plugins')
WHITELIST_PATH = os.path.join(PLUGIN_PATH, 'whitelist')
BLACKLIST_PATH = os.path.join(PLUGIN_PATH, 'blacklist')


def dump_plugin(name, content, nature_type=0):
    """

    :param name:
    :param content:
    :param nature_type:
    :return:
    """
    if not name.endswith('.py'):
        module_name = name
        name = '{0}.py'.format(name)
    else:
        module_name = name[:-3]

    if nature_type == 0:
        file_path = os.path.join(WHITELIST_PATH, name)
        module_name = 'seecode_scanner.plugins.whitelist.{0}'.format(module_name)
    else:
        file_path = os.path.join(BLACKLIST_PATH, name)
        module_name = 'seecode_scanner.plugins.blacklist.{0}'.format(module_name)

    # FIXME 检测文件是否存在
    with open(file_path, 'wt') as fp:
        fp.write(content)

    return module_name
