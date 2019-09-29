# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.shortcuts import render, HttpResponseRedirect
from django.views.decorators.csrf import ensure_csrf_cookie

from seecode.libs.core.common import clear_all_cache
from seecode.libs.dal.config import get_config
from seecode.libs.dal.config import update_config_obj
from seecode.libs.units import perm_verify
from seecode.libs.units import parse_bool
from seecode.libs.core.enum import SYSLOG_LEVEL
from seecode.libs.core.enum import MONTH_TYPE


@login_required
@ensure_csrf_cookie
@perm_verify(['system.change_settings', ])
def index(request):
    """
    :param request:
    :return:
    """

    if request.method == 'POST':
        gitlab_url = request.POST.get('gitlab_url', '')
        gitlab_token = request.POST.get('gitlab_token', '')
        gitlab_account = request.POST.get('gitlab_account', '')
        gitlab_api = request.POST.get('gitlab_api_url', '')
        gitlab_activity_month = request.POST.get('gitlab_activity_month', 12)
        sonarqube_url = request.POST.get('sonarqube_url', '')
        sonarqube_token = request.POST.get('sonarqube_token', '')
        upload_type = request.POST.get('upload_type', 1)
        local_upload_root = request.POST.get('local_upload_root', '')
        ftp_host = request.POST.get('ftp_host', '')
        ftp_username = request.POST.get('ftp_username', '')
        ftp_password = request.POST.get('ftp_password', '')
        ftp_path = request.POST.get('ftp_path', '')
        ftp_port = request.POST.get('ftp_port', 21)
        upload_file_type = request.POST.get('upload_file_type', '')
        upload_file_size = request.POST.get('upload_file_size', '')
        seecode_workdir = request.POST.get('seecode_workdir', '')
        seecode_sys_level = request.POST.get('seecode_sys_level', '')
        seecode_domain = request.POST.get('seecode_domain', '')
        seecode_node_secret = parse_bool(request.POST.get('seecode_node_secret', False))

        cache.set('seecode_conf', None, 0)
        conf = get_config()

        if not conf:
            conf = {
                'gitlab': {},
                'sonarqube': {},
                'option': {},
                'sync': {},
                'project': {}
            }
        if gitlab_url:
            conf['gitlab']['url'] = gitlab_url.strip()
        if gitlab_token:
            conf['gitlab']['token'] = gitlab_token.strip()
        if gitlab_account:
            conf['gitlab']['account'] = gitlab_account.strip()
        if gitlab_api:
            conf['gitlab']['api_url'] = gitlab_api.strip()
        if gitlab_activity_month:
            conf['gitlab']['activity_month'] = int(gitlab_activity_month)
        if sonarqube_url:
            conf['sonarqube']['url'] = sonarqube_url.strip()
        if sonarqube_token:
            conf['sonarqube']['token'] = sonarqube_token.strip()

        if seecode_workdir:
            conf['option']['seecode_workdir'] = seecode_workdir.strip()
        if seecode_sys_level:
            conf['option']['seecode_sys_level'] = int(seecode_sys_level)

        conf['option']['seecode_node_secret'] = seecode_node_secret
        conf['option']['seecode_domain'] = seecode_domain

        if upload_type:
            conf['project']['upload_type'] = int(upload_type)  # 1 local 2 ftp
        if local_upload_root:
            conf['project']['upload_root'] = local_upload_root.strip()
        if ftp_host:
            conf['project']['ftp_host'] = ftp_host.strip()
        if ftp_username:
            conf['project']['ftp_username'] = ftp_username.strip()
        if ftp_password:
            conf['project']['ftp_password'] = ftp_password.strip()
        if ftp_path:
            conf['project']['ftp_path'] = ftp_path.strip()
        if ftp_port:
            conf['project']['ftp_port'] = int(ftp_port)
        if upload_file_type:
            conf['project']['upload_file_type'] = upload_file_type.strip()
        if upload_file_size:
            conf['project']['upload_file_size'] = int(upload_file_size)

        update_config_obj(
            config_id=1,
            content=str(conf)
        )

        return HttpResponseRedirect('/sys/settings/')
    else:
        conf = get_config()
        return render(request, 'system/settings.html', {
            'nav': 'sys',
            'conf': conf,
            'log_type': SYSLOG_LEVEL,
            'month_type': MONTH_TYPE,
        })


@login_required
@ensure_csrf_cookie
def clear_cached(request):
    """
        :param request:
        :return:
    """
    clear_all_cache()

    return HttpResponseRedirect('/sys/settings')
