# coding: utf-8

import hashlib
import os
import time

from django.conf import settings
from django.core.cache import cache
from django.db import connections

from seecode.libs.core.common import make_dir
from seecode.libs.core.common import hash_md5


def parse_int(str_value, default_value=0):
    """
    转换成int
    :param str_value:
    :param default_value:
    :return:
    """
    if str_value:
        try:
            result = int(str_value)
        except (ValueError, TypeError):
            result = default_value
    else:
        result = default_value
    return result


def parse_bool(str_value):
    """
    转换成 bool
    :param str_value:
    :return:
    """
    if str_value == 'on' or str_value:
        return True
    else:
        return False


def strip(str_value):
    if str_value:
        return str_value.strip()
    else:
        return str_value


def close_old_connections():
    for conn in connections.all():
        conn.close_if_unusable_or_obsolete()


def handle_uploaded_file(f, save_path):
    with open(save_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def perm_verify(perms_list):
    """
    Decorator to make a view only accept particular request methods.  Usage::

        @require_http_methods(["GET", "POST"])
        def my_view(request):
            # I can assume now that only GET or POST requests make it this far
            # ...

    Note that request methods should be in uppercase.
    """
    def decorator(func):
        def inner(request, *args, **kwargs):
            current_perm = request.session.get('perm', None)

            #if not current_perm:
            #    return HttpResponseForbidden()

            #if isinstance(perms_list, list):
            #    for perm in perms_list:
            #        if perm not in current_perm:
            #            return HttpResponseForbidden()

            return func(request, *args, **kwargs)
        return inner
    return decorator


def upload_file(file_stream, save_relative_path, customize_save_path=None, random_filename=True):
    """

    :param file_stream:
    :param save_relative_path: 使用内置的上传路径
    :param customize_save_path: 自定义上传路径
    :param random_filename: 是否随机上传文件名
    :return:
    """
    _, ext = os.path.splitext(file_stream.name)
    if random_filename:
        file_name = '{0}{1}'.format(str(int(time.time())), ext)
    else:
        file_name = '{0}{1}'.format(_, ext)
    if not customize_save_path:
        absolute_path = '{0}{1}'.format(settings.MEDIA_ROOT, save_relative_path)
    else:
        absolute_path = customize_save_path
    make_dir(absolute_path)
    full_upload_file = os.path.join(absolute_path, file_name)
    handle_uploaded_file(file_stream, full_upload_file)
    relative_path_file = os.path.join(save_relative_path, file_name)

    return relative_path_file, full_upload_file


def get_file_content(full_file_path):
    """

    :param full_file_path:
    :return:
    """
    cache_key = 'scan_files:{0}'.format(hash_md5(full_file_path))
    result = cache.get(cache_key)
    if result:
        return result

    with open(full_file_path, 'rt') as fp:
        result = fp.readlines()
        cache.set(cache_key, result, 60*15)

    return result


def md5sum(fname):
    """
    计算文件的MD5值
    :param fname:
    :return:
    """
    def read_chunks(fh):
        fh.seek(0)
        chunk = fh.read(8096)
        while chunk:
            yield chunk
            chunk = fh.read(8096)
        else:  # 最后要将游标放回文件开头
            fh.seek(0)

    m = hashlib.md5()
    if isinstance(fname, str) and os.path.exists(fname):
        with open(fname, "rb") as fh:
            for chunk in read_chunks(fh):
                m.update(chunk)

    # 上传的文件缓存 或 已打开的文件流
    elif fname.__class__.__name__ in ["StringIO", "StringO"]:
        for chunk in read_chunks(fname):
            m.update(chunk)
    else:
        return ""

    return m.hexdigest()


def get_tactic_type_scope(type_id):
    """

    :param type_id:
    TACTIC_TYPE = (
        (1, u"Bug"),
        (2, u"Code Smell"),
        (3, u"Vulnerability"),
    )

    :return:
    """

    result = 0.0
    if type_id == 1:
        result = 2.0
    elif type_id == 2:
        result = 1.0
    elif type_id == 3:
        result = 3.0

    return result


def get_tactic_risk_scope(risk_id):
    """

    :param risk_id:
    RISK_TYPE = (
        (1, u"严重"),  # BLOCKER, critical
        (2, u"高危"),  # BLOCKER, high
        (3, u"中危"),  # CRITICAL, medium
        (4, u"低危"),  # MAJOR, low
        (5, u"信息"),  # BLOCKER, info
    )
    :return:
    """
    result = 0
    if risk_id == 1:
        result = 4.0
    elif risk_id == 2:
        result = 3.0
    elif risk_id == 3:
        result = 2.0
    elif risk_id == 4:
        result = 1.0

    return result


def get_tactic_tag_scope(tags):
    """

    :param tags:

    :return:
    """
    scope = {
        '0.03': ['RCE', 'SSRF', 'RFL', 'SQLI', 'XSS', '已知组件漏洞'],
        '0.02': ['LFL', 'SSTI', 'RXSS', '安全配置缺失', '信息泄露'],
        '0.01': [],
    }
    total_scope = 0.0

    for tag in tags:
        found_tag = False
        for k, v in scope.items():
            if tag.upper() in v:
                total_scope += float(k)
                found_tag = True
        if not found_tag:
            total_scope += 0.01

    return total_scope


def get_scope_level(scope):
    """

    :param scope:

    :return:
    """
    level = '安全'

    scope = round(float(scope), 2)

    if scope >= 7.0:
        level = '高风险'
    elif scope >= 5.0 and scope < 7.0:
        level = '警告'
    elif scope >= 2.0 and scope < 5.0:
        level = '低风险'
    elif scope >= 0 and scope < 2.0:
        level = '安全'
    return level
