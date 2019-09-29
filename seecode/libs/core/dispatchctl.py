# coding: utf-8

from seecode.apps.project.models.item import ProjectInfo
from seecode.libs.core.exceptions import ApplicationNotFound
from seecode.libs.core.exceptions import ScanTaskAlreadyExists
from seecode.libs.core.exceptions import TaskConfCreateException
from seecode.libs.core.enum import task_type as tasktype
from seecode.libs.dal.application import get_app_by_branch
from seecode.libs.dal.application import get_app_by_id
from seecode.libs.dal.config import get_config
from seecode.libs.dal.gitlab_project import get_project_list_by_group_id
from seecode.libs.dal.scan_task import _get_task_obj
from seecode.libs.dal.scan_task import create_task_by_app_id
from seecode.libs.dal.scan_task import create_task_by_project
from seecode.libs.dal.scan_task import get_task_by_id
from seecode.libs.dal.scan_task import update_task_config
from seecode.libs.dal.scan_task import update_task_failed
from seecode.libs.dal.syslog import create_syslog_obj
from seecode_scanner.tasks.scan import start as seecode_scanner_start


def send_task(task_id):
    """
    :return:
    """
    t_conf = TaskConf(task_id=task_id)
    seecode_scanner_start.delay(**t_conf.config)


def create_scan_task(**kwargs):
    """

    :param kwargs:
    :return:
    """
    task_group_id = kwargs.get('task_group_id')
    app_id = kwargs.get('app_id')
    project_id = kwargs.get('project_id')
    branch = kwargs.get('branch')
    is_force_scan = kwargs.get('is_force_scan', False)
    scan_way = kwargs.get('scan_way', 1)
    version = kwargs.get('version', '')

    if app_id:
        task_obj = create_task_by_app_id(
            app_id=app_id,
            group_id=task_group_id,
            is_force_scan=is_force_scan,
            scan_way=scan_way,
            version=version,
        )
    else:
        task_obj = create_task_by_project(
            project_id=project_id,
            branch=branch,
            group_id=task_group_id,
            is_force_scan=is_force_scan,
            scan_way=scan_way,
            version=version,
        )
    return task_obj


class TaskConf(object):
    """
    创建扫描任务的配置文件
    """

    def __init__(self, task_id):
        """

        :param task_id:
        """
        self.task = get_task_by_id(task_id=task_id)
        if not self.task:
            raise TaskConfCreateException('Task not found, id:{0}.'.format(task_id))

        self.sys_conf = get_config()
        self.app = self.task.app
        self.project = self.app.project
        self.group = self.project.group
        self.repo = self.app.repo
        self.profile = self.task.group.profile

        log_level = 'info'

        if self.sys_conf['option']['seecode_sys_level'] == 1:
            log_level = 'error'
        elif self.sys_conf['option']['seecode_sys_level'] == 2:
            log_level = 'error'
        elif self.sys_conf['option']['seecode_sys_level'] == 3:
            log_level = 'warning'
        elif self.sys_conf['option']['seecode_sys_level'] == 4:
            log_level = 'info'
        elif self.sys_conf['option']['seecode_sys_level'] == 5:
            log_level = 'debug'

        storage_type = 'local'

        s_t = self.sys_conf['project']['upload_type']

        if s_t == 1:
            storage_type = 'local'
        elif s_t == 2:
            storage_type = 'ftp'

        self._task_conf = {
            'task_id': self.task.id,
            'template': self.profile.name,
            'log_level': log_level,
            'work_dir': self.sys_conf['option']['seecode_workdir'],
            'project_name': self.project.name or '',
            'project_branch': self.repo.name or '',
            'project_ssh': self.project.ssh_url_to_repo or self.project.path,
            'project_web': self.project.web_url or '',
            'project_file_origin_name': self.project.file_origin_name or '',
            'project_file_hash': self.project.file_hash or '',
            'group_name': self.group.name or '',
            'group_key': self.group.path or '',
            'project_type': 'online' if self.project.type == 1 else 'offline',
            'project_storage_type': storage_type,
            'evidence_start_line_offset': -1,
            'evidence_count': 5,
            'result_file': '{0}.json'.format(self.task.id),
            'sync_vuln_to_server': True,
            'force_sync_code': self.task.is_force_scan,
        }

        update_task_config(
            task_id=self.task.id,
            config=str(self._task_conf),
        )

    @property
    def config(self):
        return self._task_conf


def dispatch_task(**kwargs):
    """
    派发扫描任务服务
    :param kwargs:
    :return:
    """
    task_obj = None
    try:
        task_group_id = kwargs.get('task_group_id', None)
        task_type = kwargs.get('task_type', None)
        group_id = kwargs.get('group_id', None)
        app_id = kwargs.get('app_id', None)
        branch = kwargs.get('branch', '')
        is_force_scan = kwargs.get('is_force_scan', False)
        scan_way = kwargs.get('scan_way', 1)

        if not all((task_group_id,)):
            raise Exception("任务分组不能为空!")

        if task_type == tasktype.SINGLE:  # 单项目
            check_scan_task(app_id=app_id)
            task_obj = create_scan_task(
                task_group_id=task_group_id,
                app_id=app_id,
                is_force_scan=is_force_scan,
                scan_way=scan_way,
            )
            send_task(task_id=task_obj.id)
        else:
            if task_type == tasktype.MULTIPLE:  # 指定项目组
                if not group_id:
                    raise Exception("分组未找到，ID:{0}．".format(group_id))
                project_list = get_project_list_by_group_id(group_id=group_id)
            else:  # 所有项目组
                project_list = ProjectInfo.objects.all()

            for item in project_list:
                try:
                    app_obj = get_app_by_branch(name=branch, project_id=item.id)
                    if app_obj:
                        check_scan_task(app_id=app_obj.id)
                        task_obj = create_scan_task(
                            task_group_id=task_group_id,
                            app_id=app_obj.id,
                            is_force_scan=is_force_scan,
                            scan_way=scan_way,
                        )
                        send_task(task_id=task_obj.id)
                    else:
                        raise ApplicationNotFound('未找到 branch name:{0}, project id: {1} 对应的应用。'.format(branch, item.id))
                except (ScanTaskAlreadyExists, ApplicationNotFound) as ex:
                    import traceback;
                    traceback.print_exc()
                    create_syslog_obj(
                        title='创建扫描任务失败',
                        description=str(ex),
                        stack_trace=traceback.format_exc(),
                        level=2,
                        is_read=False,
                    )
        return True
    except (ScanTaskAlreadyExists, ApplicationNotFound) as ex:
        import traceback
        traceback.print_exc()
        create_syslog_obj(
            title='创建扫描任务失败',
            description=str(ex),
            stack_trace=traceback.format_exc(),
            level=2,
            is_read=False,
        )
        return False
    except Exception as ex:
        import traceback;
        traceback.print_exc()
        if task_obj:
            update_task_failed(
                task_id=task_obj.id,
                title=str(ex),
                reason=traceback.format_exc()
            )
        create_syslog_obj(
            title='创建扫描任务失败',
            description=str(ex),
            stack_trace=traceback.format_exc(),
            level=1,
            is_read=False,
        )
        return False


def check_scan_task(app_id):
    """

    :return:
    """
    task_obj = _get_task_obj(app_id=app_id, status=[2, 3, 4, 5])
    if task_obj:
        app_obj = get_app_by_id(app_id=app_id)
        raise ScanTaskAlreadyExists("＂{0}＂扫描任务已存在，请等待其执行完成．".format(app_obj.app_name))
