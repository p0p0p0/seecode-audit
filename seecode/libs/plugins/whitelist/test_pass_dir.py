# coding: utf-8

import os
import re

REGEX_CHECK_LIST = [
    re.compile('/test/', re.I),  # case: modules/manager-base/src/test/java/com/example/test/ad/AdTest.java
    re.compile('^test/', re.I),  # case: test/test_utils.py
    re.compile('^test', re.I),  # case: api/test_utils.py
]


def run(full_file_path):
    """
    入口函数
    :param full_file_path:
    :return:
    """
    # logger.debug('Test "{0}" whitelist plugin ...'.format(__NAME__))

    # 开始测试白名单规则
    return _test_path_rule(full_file_path)


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
