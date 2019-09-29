# coding: utf-8

import re
import os

__NAME__ = '测试文件与测试目录跳过扫描'
__AUTHOR__ = ''
__VERSION__ = '0.2'
__RISK__ = 1
__KBID__ = ''


REGEX_CHECK_LIST = [
    re.compile('/test/', re.I),  # case: modules/manager-base/src/test/java/com/example/test/ad/AdTest.java
    re.compile('^test/', re.I),  # case: test/test_utils.py
    re.compile('^test', re.I),  # case: api/test_utils.py
]


def run(**kwargs):
    """
    入口函数
    :param kwargs:
    :return:
    """
    # logger.debug('Test "{0}" whitelist plugin ...'.format(__NAME__))
    code_path = kwargs.get('code_path', None)
    title = kwargs.get('title', None)
    file_name = kwargs.get('file_name', None)
    start_line = kwargs.get('start_line', None)
    end_line = kwargs.get('end_line', None)
    file_content = kwargs.get('file_content', None)

    # 开始测试白名单规则
    return _test_path_rule(file_name)


def _test_path_rule(file_path):
    """
    规则测试
    :param file_path: 文件路径
    :return:
    """
    result = False

    # regex
    if REGEX_CHECK_LIST:
        for item in set(REGEX_CHECK_LIST):
            # FIXME Bypass
            _, filename = os.path.split(file_path)  # pass 文件名中包含 test 的
            if item.search(file_path) or item.search(filename):
                return True

    return result
