# coding: utf-8
from __future__ import unicode_literals

import os
import shutil

import pinyin
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from pytz import timezone

from seecode.apps.project.models.app import ApplicationInfo
from seecode.apps.project.models.item import ProjectHistoryInfo
from seecode.apps.project.models.item import ProjectInfo
from seecode.apps.project.models.item import RepositoryInfo
from seecode.libs.core.cache_key import PROJECT_INFO_CACHE
from seecode.libs.core.common import del_file
from seecode.libs.core.common import make_dir
from seecode.libs.core.enum import PROJECT_TYPE
from seecode.libs.core.enum import icon_type
from seecode.libs.dal.application import get_app_by_branch
from seecode.libs.dal.config import get_config
from seecode.libs.dal.gitlab_group import get_group_all_member_perm
from seecode.libs.dal.gitlab_group import get_group_by_id
from seecode.libs.dal.gitlab_project import create_project_obj
from seecode.libs.dal.gitlab_project import get_pro_all_member_perm
from seecode.libs.dal.gitlab_project import get_project_by_id
from seecode.libs.dal.gitlab_repository import create_repository_obj
from seecode.libs.dal.project_history import create_pro_history_obj
from seecode.libs.paginator import Paginator
from seecode.libs.units import md5sum
from seecode.libs.units import parse_int
from seecode.libs.units import upload_file
from seecode.libs.utils.ftpwrapper import FTPWork

tz = timezone('Asia/Shanghai')


@login_required
@ensure_csrf_cookie
def index(request):
    """
    :param request:
    :return:
    """
    if request.method == 'POST':
        create_project(request)
        return HttpResponseRedirect('/project/')
    else:
        lang = request.GET.get('l', '')
        group_id = request.GET.get('g', '')
        project_id = request.GET.get('_p', '')
        status = request.GET.get('s', '')
        archive = request.GET.get('archive', '')

        page_num = parse_int(request.GET.get('p', 1), 1)
        page_size = parse_int(request.GET.get('ps', 20), 20)
        group_obj = None
        project_obj = None

        sql_where = {
            'is_archive': False
        }
        if lang:
            sql_where['lang'] = lang
        if group_id:
            group_obj = get_group_by_id(group_id=group_id)
            sql_where['group__id'] = int(group_id)
        if project_id:
            project_obj = get_project_by_id(project_id=project_id)
            sql_where['id'] = int(project_id)
        if status:
            status = int(status)
            sql_where['type'] = status
        if archive == '1':
            sql_where['is_archive'] = True

        items = ProjectInfo.objects.filter(**sql_where).order_by('-updated_at')
        paginator = Paginator(items, page_size, request=request, pre_name=u"项目")
        page = paginator.page(page_num)

        return render(request, 'project/item/index.html', {
            'nav': 'pro',
            'page': page,
            'lang': lang,
            'group_obj': group_obj,
            'project_obj': project_obj,
            'project_type': PROJECT_TYPE,
            's': status,
            'archive': archive,
        })


@login_required
@ensure_csrf_cookie
def show(request, project_id):
    """
    :param request:
    :param project_id:
    :return:
    """
    if request.method == 'POST':
        model = ProjectInfo.objects.get(id=project_id)
        dept_id = request.POST.get('dept', '')
        dept_obj = get_dept_by_id(dept_id)
        if dept_obj and model:
            if model.department and model.department.id != dept_obj.id or not model.department:
                if model.department:
                    old_dept = '{0}/{1}'.format(model.department.parent_nodes_name, model.department)
                else:
                    old_dept = '<空>'
                model.department = dept_obj
                model.save()
                cache.set('{0}:{1}'.format(PROJECT_INFO_CACHE[1], model.id), None, 0)
                cache.set('{0}:{1}'.format(PROJECT_INFO_CACHE[1], model.ssh_url_to_repo), None, 0)
                cache.set('{0}:{1}'.format(PROJECT_INFO_CACHE[2], model.git_id), None, 0)
                create_pro_history_obj(
                    project_obj=model,
                    type=icon_type.ORGANIZATION,
                    user=request.user,
                    title='所属部门变更',
                    description='变更内容：从  “{0}” 修改为  “{1}” 部门，操作人: {2}。'.format(
                        old_dept, '{0}/{1}'.format(dept_obj.parent_nodes_name, dept_obj.name), request.user
                    )
                )

        return HttpResponseRedirect("/project/{0}/".format(project_id))
    else:
        try:
            default_branch_app = ''
            model = ProjectInfo.objects.get(id=project_id)
            repo_list = RepositoryInfo.objects.filter(project__id=int(project_id))
            app_list = ApplicationInfo.objects.filter(project__id=int(project_id))
            if model.default_branch:
                default_branch_app = get_app_by_branch(name=model.default_branch, project_id=model.id)
            project_members = get_pro_all_member_perm(project_id)
            group_members = get_group_all_member_perm(model.group.id)
            member_count = len(project_members) + len(group_members)
            history_list = ProjectHistoryInfo.objects.filter(project__id=project_id).order_by('-created_at')[:15]
            changelog_groups = {}
            for item in history_list:
                date = item.created_at.astimezone(tz).strftime('%Y-%m-%d')
                if date not in changelog_groups:
                    changelog_groups[date] = []
                changelog_groups[date].append(item)

        except ProjectInfo.DoesNotExist as ex:
            return HttpResponseRedirect('/project/?errmsg={0}'.format(u'项目未找到!'))

        return render(request, 'project/item/edit.html', {
            'nav': 'pro',
            'model': model,
            'repo_list': repo_list,
            'app_list': app_list,
            'default_branch_app': default_branch_app,
            'project_members': project_members,
            'group_members': group_members,
            'member_count': member_count,
            'history_list': history_list,
            'changelog_groups': changelog_groups,
        })


@login_required
def create_project(request):
    """
    :param request:
    :return:
    """
    name = request.POST.get('name', '')
    group = request.POST.get('group', '')
    project_type = request.POST.get('type', '')
    ssh_url = request.POST.get('ssh_url', '')
    upload = request.FILES.get('upload', '')
    description = request.POST.get('description', '')
    conf = get_config()

    if project_type == '1':  # 线上
        if not all((ssh_url, name, group)):
            raise Exception('缺少"ssh_url, name, group"关键参数。')
        group_obj = get_group_by_id(group_id=group)
        key = pinyin.get(name.strip(), format='strip', delimiter="")
        proj_obj = create_project_obj(
            group_obj=group_obj,
            default_branch='master',
            name=name.strip(),
            path=key,
            description=description.strip(),
            ssh_url_to_repo=ssh_url.strip(),
            type=project_type,
            is_new=False,
            user=request.user,
        )
        if proj_obj:
            create_repository_obj(
                name='master',
                project_obj=proj_obj,
            )
    else:
        if not all((upload, name, group)):
            raise Exception('缺少"upload, name, group"关键参数。')
        file_name, ext = os.path.splitext(upload.name)
        if ext not in conf['project']['upload_file_type']:
            raise Exception('不允许上传 {0} 格式问题。'.format(ext))
        save_path, full_save_path = upload_file(file_stream=upload, save_relative_path='/projects')
        file_size = upload.size
        group_obj = get_group_by_id(group_id=group)
        hash_md5 = md5sum(full_save_path)
        file_origin_name = '{0}{1}'.format(file_name, ext)
        if conf['project']['upload_type'] == 1:
            file_path = os.path.join(conf['project']['upload_root'], group_obj.path.upper(), name.strip())
            make_dir(file_path)
            path = os.path.join(file_path, os.path.basename(full_save_path))
            shutil.move(full_save_path, path)
        else:
            try:
                ftp = FTPWork(
                    host=conf['project']['ftp_host'],
                    port=conf['project']['ftp_port'],
                    username=conf['project']['ftp_username'],
                    password=conf['project']['ftp_password'],
                )
                ftp_path = os.path.join(conf['project']['ftp_path'], 'projects', group_obj.path.upper())
                status, _ = ftp.make_dir(ftp_path)
                ftp_full_path = '{0}/{1}'.format(ftp_path, os.path.basename(full_save_path))
                status, _ = ftp.upload_file(full_save_path, ftp_full_path)
                if not status:
                    raise Exception('FTP上传文件失败，原因：{0}'.format(_))
                path = 'ftp://{0}:{1}{2}'.format(
                    conf['project']['ftp_host'],
                    conf['project']['ftp_port'],
                    ftp_full_path,
                )
                del_file(full_save_path)
            except Exception as ex:
                raise ex

        proj_obj = create_project_obj(
            group_obj=group_obj,
            default_branch='master',
            name=name.strip(),
            path=path,
            description=description.strip(),
            type=project_type,
            is_new=False,
            user=request.user,
            file_size=file_size,
            file_hash=hash_md5,
            file_origin_name=file_origin_name,
        )
        create_repository_obj(
            name='master',
            project_obj=proj_obj,
        )
    return True


@login_required
@ensure_csrf_cookie
def batch(request):
    """
    :param request:
    :return:
    """
    action = request.POST.get('action', '')
    ids = request.POST.get('ids', '')
    dep_id = request.POST.get('dep_id', '')

    try:
        if action == 'del':
            ProjectInfo.objects.filter(id__in=[i for i in ids.split(',') if i]).delete()
        elif action == 'archive':
            ProjectInfo.objects.filter(id__in=[i for i in ids.split(',') if i]).update(is_archive=True)
            ApplicationInfo.objects.filter(project__id__in=[i for i in ids.split(',') if i]).update(is_archive=True)
        elif action == 'unarchive':
            ProjectInfo.objects.filter(id__in=[i for i in ids.split(',') if i]).update(is_archive=False)
            ApplicationInfo.objects.filter(project__id__in=[i for i in ids.split(',') if i]).update(is_archive=False)
        elif action == 'update_dept':
            pass
        return JsonResponse({"status": "ok"}, safe=False)
    except Exception as ex:
        import traceback;
        traceback.print_exc()
        return JsonResponse({"status": "failed", 'msg': str(ex)}, safe=False)
