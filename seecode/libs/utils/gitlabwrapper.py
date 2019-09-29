# coding: utf-8

import datetime

import gevent
from gevent.threadpool import ThreadPool
from pytz import timezone

from seecode.libs.core.common import utc2local
from seecode.libs.core.data import logger
from seecode.libs.core.enum import LOG_LEVEL
from seecode.libs.core.enum import icon_type
from seecode.libs.dal.config import get_config
from seecode.libs.dal.gitlab_group import create_group_member_perm_obj
from seecode.libs.dal.gitlab_group import create_group_obj
from seecode.libs.dal.gitlab_group import create_or_update as group_create_or_update
from seecode.libs.dal.gitlab_group import get_group_by_gitid
from seecode.libs.dal.gitlab_group import get_group_member_perm
from seecode.libs.dal.gitlab_group import update_group_obj
from seecode.libs.dal.gitlab_member import create_or_update
from seecode.libs.dal.gitlab_member import get_member_by_gitid
from seecode.libs.dal.gitlab_project import create_or_update as project_create_or_update
from seecode.libs.dal.gitlab_project import create_pro_member_perm_obj
from seecode.libs.dal.gitlab_project import get_pro_member_perm
from seecode.libs.dal.gitlab_project import get_project_by_gitid
from seecode.libs.dal.gitlab_repository import create_repository_obj
from seecode.libs.dal.gitlab_repository import get_repository_by_name
from seecode.libs.dal.gitlab_repository import update_repository_obj
from seecode.libs.dal.project_history import create_pro_history_obj
from seecode.libs.dal.syslog import create_syslog_obj
from seecode.libs.utils.api_gitlab import GitlabAPIHandler


class GitLabOperator(object):

    def __init__(self):
        """
        """
        conf = get_config()
        if not conf:
            raise Exception(u'配置文件读取失败!')
        self.api = GitlabAPIHandler(api_url=conf['gitlab']['api_url'], token=conf['gitlab']['token'])
        self.activity_limit_month = conf['gitlab']['activity_month'] or 12
        self.tz = timezone('Asia/Shanghai')
        self.pool = ThreadPool(20)

    def add_groups(self):
        """

        添加项目分组
        :return:
        """
        logger.info('Start syncing project group information...')
        groups = self.api.get_groups()
        for group in groups:
            group_obj = group_create_or_update(
                git_id=group['id'],
                name=group['name'],
                path=group['path'],
                description=group['description'],
                web_url=group['web_url'],
                full_name=group['full_name'],
                full_path=group['full_path'],
                visibility_level=group['visibility_level'],
            )
            if group_obj:
                logger.debug('group name:{0}, group path:{1}'.format(group['name'], group['path']))
            yield group_obj

    def _add_groups_members(self, group_obj):
        """

        :param group_obj:
        :return:
        """
        members = self.api.get_members_by_group(group_id=group_obj.git_id)
        for member in members:
            if 'email' in member:
                email = member['email']
            else:
                email = None

            m = get_member_by_gitid(member['id'])
            if not m or m.state != 'active':
                member_obj = create_or_update(
                    git_id=member['id'],
                    name=member['name'],
                    username=member['username'],
                    state=member['state'],
                    web_url=member['web_url'],
                    email=email,
                )
                if member_obj:
                    logger.info('[FOUND] username: {0}, git id:{1}'.format(member['username'], member['id']))
                    if not group_obj.members.filter(git_id=member['id']).exists():
                        group_obj.members.add(member_obj)
                    perm = get_group_member_perm(member_id=member_obj.id, group_id=group_obj.id)
                    if not perm:
                        create_group_member_perm_obj(
                            group_obj=group_obj,
                            member_obj=member_obj,
                            access_level=member['access_level'],
                            expires_at=member['expires_at']
                        )

    def add_groups_and_members(self):
        """

        FBI WARNING!!! Do not use, Do not use, Do not use.
        :return:
        """
        for group_obj in self.add_groups():
            self.pool.spawn(self._add_groups_members, group_obj)
        gevent.wait()

    def add_projects(self, enable_sync_branch=True):
        """
        添加项目
        :return:
        """
        logger.info('Start syncing project information...')
        today = datetime.datetime.now()
        for project in self.api.get_projects():
            last_activity_at = utc2local(project['last_activity_at']) + datetime.timedelta(
                days=self.activity_limit_month * 30)
            if last_activity_at < today:
                logger.warn('[SKIP] “{0}” 项目已超过 {1} 个月未活动, 跳过当前项目的信息同步, 最后活动时间: {2}。'
                            ''.format(project['name'], self.activity_limit_month, project['last_activity_at']))
                continue
            logger.info('Start syncing "{0}" project member information ...'.format(project['name']))
            try:
                # member
                members = self._add_members_by_project(project['id'], project['name'])

                # group
                group_obj = get_group_by_gitid(git_id=project['namespace']['id'])
                if not group_obj:
                    logger.debug('"{0}" group not found.'.format(project['namespace']))
                    group_obj = create_group_obj(
                        git_id=project['namespace']['id'],
                        name=project['namespace']['name'],
                        parent_id=project['namespace']['parent_id'],
                        path=project['namespace']['path'],
                        full_path=project['namespace']['full_path'],
                    )
                    group_json = self.api.get_group_info(group_id=project['namespace']['id'])
                    if group_json:
                        group_obj = update_group_obj(
                            git_id=group_json['id'],
                            name=group_json['name'],
                            path=group_json['path'],
                            description=group_json['description'],
                            web_url=group_json['web_url'],
                            full_name=group_json['full_name'],
                            full_path=group_json['full_path'],
                            visibility_level=group_json['visibility_level'],
                        )
                        self._add_groups_members(group_obj)

                # project
                pro = get_project_by_gitid(project['id'])
                i_ok = False
                if pro:
                    last_activity_at = utc2local(project['last_activity_at']).strftime("%Y%m%d%H%M%S")
                    pro_last_activity_at = utc2local(pro.git_last_activity_at.astimezone(self.tz).strftime("%Y-%m-%d %H:%M:%S")).strftime("%Y%m%d%H%M%S")
                    # assert last_activity_at == pro_last_activity_at
                    # assert project['name'].lower() == pro.name.lower()
                    # assert project['ssh_url_to_repo'].lower() == pro.ssh_url_to_repo.lower()
                    if last_activity_at != pro_last_activity_at or \
                            project['name'].lower() != pro.name.lower() or \
                            project['ssh_url_to_repo'].lower() != pro.ssh_url_to_repo.lower():
                        i_ok = True
                else:
                    i_ok = True
                if not project['default_branch'] and pro:
                    i_ok = False
                    logger.warning('"{0}" is an empty project.'.format(project['web_url']))
                if not i_ok:
                    logger.warning('[SKIP] [*] The project has not been changed, skip the update.')
                    continue
                _name, _username, department = 'id: {0}'.format(project['creator_id']), '', None
                project_obj = project_create_or_update(
                    group_obj=group_obj,
                    git_id=project['id'],
                    git_created_at=project['created_at'],
                    git_last_activity_at=project['last_activity_at'],
                    issues_enabled=project['issues_enabled'],
                    ssh_url_to_repo=project['ssh_url_to_repo'],
                    http_url_to_repo=project['http_url_to_repo'],
                    web_url=project['web_url'],
                    default_branch=project['default_branch'],
                    name=project['name'],
                    path=project['path'],
                    path_with_namespace=project['path_with_namespace'],
                    creator_id=project['creator_id'],
                    description=project['description'],
                    star_count=project['star_count'],
                    forks_count=project['forks_count'],
                    open_issues_count=0,
                    visibility_level=project['visibility_level'],
                )

                if pro:
                    title = '更新『{0}』项目'.format(project['name'])
                    description = '更新『{0}』项目成功，默认分支：{1}'.format(
                        project['name'], project['default_branch'] or '-'
                    )
                    create_pro_history_obj(
                        project_obj=pro,
                        title=title,
                        description=description,
                        type=icon_type.INFO
                    )
                else:
                    title = '创建 『{0}』项目'.format(project['name'])
                    description = '创建『{0}』项目成功\n所属分组: {1}\n创建者：{2}({3})\n默认分支：{4}'.format(
                        project['name'], project['namespace']['name'],
                        _name, _username, project['default_branch'] or '-'
                    )
                    create_pro_history_obj(
                        project_obj=project_obj,
                        title=title,
                        description=description,
                        is_first=True,
                        type=icon_type.DATABASE
                    )

                logger.debug('[PROJECT] project name:"{0}", git id: {1}, group name:"{2}".'.format(
                    project['name'],
                    project['id'],
                    group_obj.name))

                # members
                new_list = []
                r_list = []
                if not project_obj:
                    project_obj = pro
                for username, item in members.items():
                    if item['obj'].state == 'active':  # 有效账户
                        perm = get_pro_member_perm(member_id=item['obj'].id, project_id=project_obj.id)
                        if not perm:
                            create_pro_member_perm_obj(
                                project_obj=project_obj,
                                member_obj=item['obj'],
                                access_level=item['json']['access_level'],
                                expires_at=item['json']['expires_at']
                            )
                        if not project_obj.members.filter(id=item['obj'].id).exists():
                            new_list.append(username)
                            r_list.append(item['obj'])
                if r_list:
                    if project_obj:
                        project_obj.members.add(*r_list)

                if new_list:
                    create_pro_history_obj(
                        project_obj=project_obj,
                        title='发现新授权员工 {0} 个'.format(len(new_list)),
                        description='发现新增：{0} 等账号'.format('、'.join([_ for _ in new_list])),
                        type=icon_type.USER
                    )
                # branch
                if enable_sync_branch:
                    self.sync_project_branch(project_id=project['id'])

            except Exception as ex:
                import traceback
                traceback.print_exc()
                logger.error(ex)
                create_syslog_obj(
                    title='同步 {0} 项目信息失败'.format(project['name']),
                    description=str(ex),
                    stack_trace=traceback.format_exc(),
                    level=LOG_LEVEL.CRITICAL,
                    is_read=False,
                )

    def _add_members_by_project(self, project_git_id, project_name):
        """
        更新会员信息
        :param project_git_id:
        :param project_name:
        :return:
        """
        members = {}
        for member in self.api.get_members_by_project(project_id=project_git_id):
            if not member:
                continue
            logger.info('[MEMBER] username: {0}, git id:{1}'.format(member['username'], member['id']))
            try:
                email = None
                if 'email' in member:
                    email = member['email']

                m = get_member_by_gitid(member['id'])
                if not m or m.state != 'active':
                    member_obj = create_or_update(
                        git_id=member['id'],
                        name=member['name'],
                        username=member['username'],
                        state=member['state'],
                        web_url=member['web_url'],
                        email=email,
                    )
                    members[member['username']] = {
                        'json': member,
                        'obj': member_obj,
                    }
            except Exception as ex:
                import traceback
                logger.error(ex)
                create_syslog_obj(
                    title='同步 {0} 项目成员失败'.format(project_name),
                    description=str(ex),
                    stack_trace=traceback.format_exc(),
                    level=LOG_LEVEL.CRITICAL,
                    is_read=False,
                )
        return members

    def sync_project_branch(self, project_id):
        """
        更新项目的分支与tag
        :return:
        """
        project_obj = get_project_by_gitid(git_id=project_id)
        try:
            new_result = []
            update_result = []
            for branch in self.api.get_branches(project_id=project_id):
                if not branch:
                    continue
                try:
                    bran = get_repository_by_name(name=branch['name'], project_id=project_obj.id)
                    if 'commit' in branch:
                        last_commit_id = branch['commit']['id']
                        last_short_id = branch['commit']['short_id']
                        last_author_email = branch['commit']['author_email']
                        last_author_name = branch['commit']['author_name']
                        last_title = branch['commit']['title'],
                    else:
                        last_commit_id = None
                        last_short_id = None
                        last_author_email = None
                        last_author_name = None
                        last_title = None
                    if bran:
                        if bran.last_commit_id != branch['commit']['id']:
                            update_repository_obj(
                                repo_id=bran.id,
                                name=branch['name'],
                                merged=branch['merged'],
                                protected=branch['protected'],
                                developers_can_push=branch['developers_can_push'],
                                developers_can_merge=branch['developers_can_merge'],
                                last_commit_id=last_commit_id,
                                last_short_id=last_short_id,
                                last_author_email=last_author_email,
                                last_author_name=last_author_name,
                                last_title=last_title,
                                project_obj=project_obj,
                            )
                            update_result.append(branch['name'])
                            logger.info('[BRANCH] update branch name:{0}, project name:{0}'.format(
                                branch['name'],
                                project_obj.name)
                            )
                    else:
                        new_result.append(branch['name'])
                        create_repository_obj(
                            name=branch['name'],
                            merged=branch['merged'],
                            protected=branch['protected'],
                            developers_can_push=branch['developers_can_push'],
                            developers_can_merge=branch['developers_can_merge'],
                            last_commit_id=last_commit_id,
                            last_short_id=last_short_id,
                            last_author_email=last_author_email,
                            last_author_name=last_author_name,
                            last_title=last_title,
                            project_obj=project_obj,
                        )
                        logger.info('[BRANCH] new branch name:{0}, project name:{0}'.format(
                            branch['name'],
                            project_obj.name)
                        )
                except Exception as ex:
                    import traceback
                    logger.error(ex)
                    create_syslog_obj(
                        title='同步 {0} 项目分支失败'.format(project_obj.name),
                        description=str(ex),
                        stack_trace=traceback.format_exc(),
                        level=LOG_LEVEL.CRITICAL,
                        is_read=False,
                    )
            if update_result:
                create_pro_history_obj(
                    project_obj=project_obj,
                    title='更新分支 {0} 个'.format(len(update_result)),
                    description='更新：{0} 分支'.format('、'.join(update_result)),
                    type=icon_type.CODE_FORK
                )
            if new_result:
                create_pro_history_obj(
                    project_obj=project_obj,
                    title='新增分支 {0} 个'.format(len(new_result)),
                    description='新增：{0} 分支'.format('、'.join(new_result)),
                    type=icon_type.TAGS
                )
        except Exception as ex:
            logger.error(ex)
