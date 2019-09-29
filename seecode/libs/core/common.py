# coding: utf-8
from __future__ import unicode_literals

import time
import os
import hashlib
import datetime
import shutil
import subprocess
import socket
import tarfile
import re

from seecode.libs.core.enum import RISK_TYPE
from seecode.libs.core.enum import TACTIC_TYPE
from seecode.libs.core.enum import BASIC_SCOPE


def exec_cmd(cmd):
    """
    执行一个命令并返回
    :param cmd:
    :return:
    """
    p = subprocess.Popen(
        cmd,
        bufsize=100000,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        close_fds=True
    )
    p.wait()
    out, cmd_err = p.communicate()
    if p.returncode != 0:
        raise Exception(cmd_err.strip())

    if out:
        out = out.strip().decode(encoding='utf-8')
    if cmd_err:
        cmd_err = cmd_err.strip().decode(encoding='utf-8')

    return out, cmd_err


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


def get_total_page(total, page_size=200):
    """

    :param total:
    :param page_size:
    :return:
    """
    total = int(total)
    page_size = int(page_size)
    total_page = total / page_size
    if total % page_size > 0:
        total_page += 1
    return int(total_page)


def get_local_date(date_time_str, date_format="%Y-%m-%d"):
    """

    :param date_time_str:
    :param date_format:
    :return:
    """

    date_time = utc2local(date_time_str)
    return date_time.strftime(date_format)


def datestr2date(date_str, date_format="%Y-%m-%d %H:%M:%S"):
    """
    time->字符串
    :param date_str:
    :param date_format:
    :return:
    """
    return datetime.datetime.strptime(date_str, date_format)


def utc2local(utc_time):
    """UTC时间转本地时间（+8:00）"""
    date_format = [
        '%Y-%m-%dT%H:%M:%S.%fZ+08:00',
        '%Y-%m-%dT%H:%M:%S.%f+08:00',
        '%Y-%m-%dT%H:%M:%S+08:00',
        '%Y-%m-%dT%H:%M:%S.%fZ',
        '%Y-%m-%dT%H:%M:%S',
        '%Y-%m-%d %H:%M:%S',
    ]
    date = None
    err = None
    for f in date_format:
        try:
            date = datetime.datetime.strptime(utc_time, f)
            continue
        except ValueError as ex:
           err = ex
    if date:
        now_stamp = time.time()
        local_time = datetime.datetime.fromtimestamp(now_stamp)
        utc_time = datetime.datetime.utcfromtimestamp(now_stamp)
        offset = local_time - utc_time
        local_st = date + offset
        return local_st
    else:
        raise err


def local2utc(local_time):
    """UTC时间转本地时间（+8:00）"""
    date = datetime.datetime.strptime(local_time, "%Y-%m-%dT%H:%M:%S.%fZ")
    now_stamp = time.time()
    local_time = datetime.datetime.fromtimestamp(now_stamp)
    utc_time = datetime.datetime.utcfromtimestamp(now_stamp)
    offset = local_time - utc_time
    local_st = date - offset
    return local_st


def is_intranet(ip):
    ret = ip.split('.')
    if len(ret) != 4:
        return True
    if ret[0] == '10':
        return True
    if ret[0] == '172' and 16 <= int(ret[1]) <= 32:
        return True
    if ret[0] == '192' and ret[1] == '168':
        return True
    if ret[0] == '127' and ret[1] == '0':
        return True
    return False


def get_localhost_ip():
    ip = None
    try:
        ip = socket.gethostbyname(socket.gethostname())
    except:
        pass
    return ip


def make_dir(paths):
    """
    创建路径
    :param paths:
    :return:
    """
    if isinstance(paths, list):
        for item in paths:
            if item and not os.path.isdir(item):
                os.makedirs(item)
    if isinstance(paths, str):
        if paths and not os.path.isdir(paths):
            os.makedirs(paths)


def clear_all_cache():
    """
    :return:
    """
    from django_redis import get_redis_connection
    get_redis_connection("default").flushall()


def hash_md5(hash_str):
    """

    :param hash_str:
    :return:
    """
    md5 = hashlib.md5()
    md5.update(hash_str)
    return md5.hexdigest()


def hash_md5_file(file_path):
    """

    :param file_path:
    :return:
    """
    if os.path.isfile(file_path):
        with open(file_path, 'rb') as fp:
            return hash_md5(fp.read())


def format_str2dict(origin_msg, sep=':'):
    """
    format string
    :param origin_msg:
    :param sep:
    :return:
    """
    result = {}
    str_list = []

    if origin_msg:

        if '\r\n' in origin_msg:
            str_list = origin_msg.split('\r\n')
        elif '\n' in origin_msg:
            str_list = origin_msg.split('\n')

        for line in str_list:
            _index = line.strip().find(sep)
            if _index != -1:
                k, v = line[:_index].strip(), line[_index+1:].strip()
            else:
                k, v = line.strip(), ''

            if k and k not in result:
                result[k] = v

    return result


def test_ip(ip_addr):
    """

    :param ip_addr:
    :return:
    """
    try:
        socket.inet_aton(ip_addr)
        return True
    except:
        return False


def test_port(port):
    """

    :param port:
    :return:
    """
    if not isinstance(port, int):
        port = int(port)

    return port > 1 and port < 65536


def get_risk_sonar_label(risk):
    """

    :param risk:
    :return:
    """
    if risk == 1:
        return 'BLOCKER'
    elif risk == 2:
        return 'CRITICAL'
    elif risk == 3:
        return 'MAJOR'
    elif risk == 4:
        return 'BLOCKER'
    else:
        return ''


def get_risk_by_severity(severity):
    """

    :param severity:
             (1, u"Blocker"),  # 最高等级，阻碍的
             (2, u"Critical"),  # 高等级，极为严重的
             (3, u"Major"),  # 较高等级，主要的；默认级别。
             (4, u"Minor"),  # 较低等级
             (5, u"Info"),  # 低等级
    :return:
    """
    if not severity:
        risk = 5
    else:
        if severity.lower() in ('blocker', 'critical'):
            risk = 1
        elif severity.lower() in ('major',):
            risk = 2
        elif severity.lower() in ('minor',):
            risk = 3
        else:
            risk = 4
    return risk


def get_issue_type_by_sonar(type_str):
    """

    :param type_str:
        (1, u"Bug"),  # 缺陷
        (2, u"Code Smell"),  # 代码坏味道
        (3, u"Vulnerability"),  # 易受攻击
    :return:
    """
    if type_str:
        type_str = type_str.replace("_", " ")
        if type_str.lower() in ('bug',):
            issue_type = 1
        elif type_str.lower() in ('code smell',):
            issue_type = 2
        elif type_str.lower() in ('vulnerability',):
            issue_type = 3
        else:
            issue_type = 3

    return issue_type


def get_risk_name(risk_id):
    """

    :param risk_id:
    RISK_TYPE = (
        (1, u"严重"),  # BLOCKER
        (2, u"高危"),  # BLOCKER
        (3, u"中危"),  # CRITICAL
        (4, u"低危"),  # MAJOR
        (5, u"信息"),  # BLOCKER
    )
    :return:
    """
    for item in RISK_TYPE:
        if risk_id and int(risk_id) == item[0]:
            return item[1]

    return ''


def get_risk_key(risk_id):
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
    result = 'info'
    if risk_id == 1:
        result = 'critical'
    elif risk_id == 2:
        result = 'high'
    elif risk_id == 3:
        result = 'medium'
    elif risk_id == 4:
        result = 'low'
    elif risk_id == 5:
        result = 'info'
    return result


def get_tactic_type(type_id):
    """

    :param type_id:
    TACTIC_TYPE = (
        (1, u"Bug"),
        (2, u"Code Smell"),
        (3, u"Vulnerability"),
    )

    :return:
    """
    for item in TACTIC_TYPE:
        if type_id and int(type_id) == item[0]:
            return item[1]

    return ''


def get_tactic_tag_scope(type_id):
    """

    :param type_id:
    TACTIC_TYPE = (
        (1, u"Bug"),
        (2, u"Code Smell"),
        (3, u"Vulnerability"),
    )

    :return:
    """
    for item in TACTIC_TYPE:
        if type_id and int(type_id) == item[0]:
            return item[1]

    return ''


def clean_dir(target_path):
    """

    :param target_path:
    :return:
    """
    result = False
    if os.path.isdir(target_path):
        try:
            shutil.rmtree(target_path)
            result = True
        except:
            pass
    return result


def del_file(file_path):
    """

    :param file_path:
    :return:
    """
    result = False
    if os.path.isfile(file_path):
        try:
            os.unlink(file_path)
            result = True
        except:
            pass
    return result


def make_tar(file_path, save_path, file_name='sca_rule.tar.gz'):
    """

    :param file_path:
    :param save_path:
    :param file_name:
    :return:
    """
    os.chdir(file_path)
    t = tarfile.open(os.path.join(save_path, file_name), "w:gz")
    for root, _dir, files in os.walk(file_path):
        for file in files:
            full_path = os.path.join(root, file)
            full_path = full_path.replace('{0}/'.format(file_path), '')
            t.add(full_path)
    t.close()


def get_project_scope(risk_statistics):
    """

    :param risk_statistics: {
                'vulnerability': {
                    '1': 0,  # critical
                    '2': 0,  # high
                    '3': 0,  # medium
                    '4': 0,  # low
                },
                'bug': {
                    '1': 0,
                    '2': 0,
                    '3': 0,
                    '4': 0,
                },
                'code smell': {
                    '1': 0,
                    '2': 0,
                    '3': 0,
                    '4': 0,
                }
            }
    :return:
    """
    def calculate_highest_risk(risk_data, risk_type):
        total_scope = 0
        for i in range(1, 5):
            risk_id = str(i)
            if risk_id in risk_data and risk_data[risk_id] > 0:
                scope = BASIC_SCOPE[risk_type][risk_id]['scope'] * risk_data[risk_id]
                min_scope = BASIC_SCOPE[risk_type][risk_id]['min']
                max_scope = BASIC_SCOPE[risk_type][risk_id]['max']
                if scope > 0:
                    if scope < min_scope:
                        scope += min_scope
                    if scope > max_scope:
                        scope = max_scope
                    total_scope += scope
                    break

        return total_scope

    total_scope = 0.0
    # vulnerability
    if 'vulnerability' in risk_statistics:
        total_scope += BASIC_SCOPE['vulnerability']['basic']
        scope = calculate_highest_risk(risk_statistics['vulnerability'], 'vulnerability')
        total_scope += scope
        if total_scope > 400.0:  # 超出范围
            return 400.0
        elif total_scope == 300:  # 没有风险
            total_scope = 0
        elif total_scope > 300:  # 危险
            return total_scope

    # bug
    if 'bug' in risk_statistics:
        total_scope += BASIC_SCOPE['bug']['basic']
        scope = calculate_highest_risk(risk_statistics['bug'], 'bug')
        total_scope += scope
        if total_scope > 300.0:  # 超出范围
            return 300.0
        elif total_scope == 200:  # 没有警告
            total_scope = 0
        elif total_scope > 200:  # 警告
            return total_scope

    # code smell
    if 'code smell' in risk_statistics:
        total_scope += BASIC_SCOPE['code smell']['basic']
        scope = calculate_highest_risk(risk_statistics['code smell'], 'code smell')
        total_scope += scope
        if total_scope <= 100:
            return 200.0

        if total_scope > 200.0:  # 超出范围
            return 25.0
        elif total_scope == 100:  # 没有安全
            total_scope = 200
        elif total_scope > 100:  # 安全
            return total_scope

    if total_scope == 0:
        total_scope = 200.0  # 安全
    return total_scope


def get_dork_query(query_str):
    """

    :param query_str: name:"fastjson" group:"test 1231231" app:"" origin:""
    :return:
    """
    result = {
        'meta': query_str,
        'data': {}
    }

    slice_word_re = re.compile(r'(\w+):\"(.*?)\"', re.I)
    rs = slice_word_re.findall(query_str)
    for item in rs:
        result['data'][item[0].lower().strip()] = item[1]

    return result

