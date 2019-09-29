# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django_celery_beat.models import PeriodicTask

from seecode.apps.node.models import HostInfo
from seecode.apps.project.models.app import ApplicationInfo
from seecode.apps.project.models.member import MemberInfo
from seecode.apps.system.models import SchedInfo
from seecode.apps.tactic.models import EngineInfo
from seecode.apps.tactic.models import TacticInfo
from seecode.libs.core.enum import BEHAVIOR_TYPE
from seecode.libs.core.enum import ISSUE_STATUS
from seecode.libs.core.enum import LOG_LEVEL
from seecode.libs.core.enum import SCAN_STATUS
from seecode.libs.core.enum import SCAN_WAY
from seecode.libs.core.enum import SYSLOG_LEVEL


@python_2_unicode_compatible
class ScanProfileInfo(models.Model):
    host = models.ForeignKey(HostInfo, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    description = models.TextField(null=True)
    exclude_dir = models.TextField(null=True)
    exclude_ext = models.TextField(null=True)
    exclude_file = models.TextField(null=True)
    exclude_java_package = models.TextField(null=True)
    config = models.TextField(null=True)
    enable_commit_issue = models.BooleanField(default=False)
    enable_auto_ignore = models.BooleanField(default=True, verbose_name='自动忽略')
    is_active = models.BooleanField(default=True)
    task_timeout = models.IntegerField(default=60 * 60 * 2)  # default: 2 hour

    tactics = models.ManyToManyField(TacticInfo, db_table='r_profile_tactic', related_name='tactic')
    engines = models.ManyToManyField(EngineInfo, db_table='r_profile_engine', related_name='engines')

    revision = models.FloatField(default=1.0)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"扫描配置"
        verbose_name_plural = verbose_name
        db_table = u'sca_scan_profile'


@python_2_unicode_compatible
class TaskGroupInfo(models.Model):
    name = models.CharField(max_length=255, null=True)
    profile = models.ForeignKey(ScanProfileInfo, on_delete=models.CASCADE)
    periodic = models.ForeignKey(PeriodicTask, null=True, on_delete=models.CASCADE)
    sched = models.ForeignKey(SchedInfo, null=True, on_delete=models.CASCADE)
    branch = models.CharField(max_length=64, null=True)  # FIXME remove
    args = models.TextField(null=True)
    is_default = models.BooleanField(default=True)
    apps = models.ManyToManyField(ApplicationInfo, db_table='r_app_group', related_name='apps')

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"任务分组"
        verbose_name_plural = verbose_name
        db_table = u'sca_scan_task_group'


@python_2_unicode_compatible
class TaskInfo(models.Model):
    app = models.ForeignKey(ApplicationInfo, on_delete=models.CASCADE, verbose_name='应用')
    group = models.ForeignKey(TaskGroupInfo, on_delete=models.DO_NOTHING)

    executor_ip = models.CharField(max_length=64, null=True)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    status = models.SmallIntegerField(choices=SCAN_STATUS, default=3)
    scan_way = models.SmallIntegerField(choices=SCAN_WAY, default=1)
    log_file = models.CharField(max_length=255, null=True)
    error_title = models.CharField(max_length=255, null=True)
    error_reason = models.TextField(null=True)
    config = models.TextField(null=True)
    hash = models.CharField(max_length=255, null=True)
    is_force_scan = models.BooleanField(default=True)
    version = models.CharField(max_length=32, null=True)
    template_name = models.CharField(max_length=32, null=True)
    template_version = models.CharField(max_length=32, null=True)

    critical = models.IntegerField(default=0)
    high = models.IntegerField(default=0)
    medium = models.IntegerField(default=0)
    low = models.IntegerField(default=0)
    info = models.IntegerField(default=0)

    dir_result_path = models.CharField(max_length=255, null=True, verbose_name='目录路径列表')
    file_result_path = models.CharField(max_length=255, null=True, verbose_name='文件路径列表')
    engines_result = models.TextField(null=True, verbose_name='引擎扫描结果')

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '"{0}" 扫描任务。'.format(self.app.app_name)

    def save(self, *args, **kwargs):
        level = None
        if 'level' in kwargs:
            level = kwargs.pop('level')
        super().save(*args, **kwargs)
        if self.error_title:
            TaskHistory(
                task=self,
                status=self.status,
                title=self.error_title,
                level=level or LOG_LEVEL.INFO,
                description=self.error_reason,
            ).save()

    class Meta:
        verbose_name = u"任务列表"
        verbose_name_plural = verbose_name
        db_table = u'sca_scan_task'


@python_2_unicode_compatible
class TaskHistory(models.Model):
    task = models.ForeignKey(TaskInfo, on_delete=models.CASCADE)
    status = models.SmallIntegerField(choices=SCAN_STATUS, default=3)
    level = models.SmallIntegerField(choices=SYSLOG_LEVEL, default=4)
    title = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = u"任务列表历史"
        verbose_name_plural = verbose_name
        db_table = u'sca_scan_task_history'


@python_2_unicode_compatible
class IssueInfo(models.Model):
    tactic = models.ForeignKey(TacticInfo, on_delete=models.CASCADE)
    app = models.ForeignKey(ApplicationInfo, on_delete=models.CASCADE)

    title = models.CharField(max_length=500, verbose_name='漏洞标题')
    file_name = models.CharField(max_length=255, null=True, verbose_name='漏洞文件')
    report_detail_url = models.CharField(max_length=500, null=True, verbose_name='漏洞文件')
    last_commit_author = models.CharField(max_length=64, null=True, verbose_name='最后提交者')
    last_commit_author_email = models.CharField(max_length=128, null=True, verbose_name='最后提交邮箱')
    last_commit = models.CharField(max_length=64, null=True, verbose_name='最后提交hash')
    risk_scope = models.FloatField(default=0, verbose_name='风险分数')
    start_line = models.IntegerField(default=0, verbose_name='开始行')
    end_line = models.IntegerField(default=0, verbose_name='结束行')
    code_segment = models.TextField(null=True, blank=True, verbose_name='代码片段')
    evidence_content = models.TextField(null=True, verbose_name='取证内容')
    is_false_positive = models.BooleanField(default=False, verbose_name='是否误报')
    whitelist_rule_id = models.IntegerField(null=True, verbose_name='白名单规则')
    is_whitelist = models.BooleanField(default=False, verbose_name='是否为白名单')

    status = models.SmallIntegerField(choices=ISSUE_STATUS, default=1)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        status = None
        comment = '等待确认。'
        user = None
        if 'comment' in kwargs:
            comment = kwargs.pop('comment')
        if 'status' in kwargs:
            status = kwargs.pop('status')
        else:
            if not isinstance(self.id, int):
                status = self.status
        if 'user' in kwargs:
            user = kwargs.pop('user')

        super().save(*args, **kwargs)

        if status:
            IssueFlowInfo(
                issue=self,
                user=user,
                behavior=2 if user else 1,
                status=self.status,
                comment=comment,
            ).save()

    class Meta:
        unique_together = ("app", "tactic", 'file_name', 'start_line')
        verbose_name = u"问题工单"
        verbose_name_plural = verbose_name
        db_table = u'sca_issue'


@python_2_unicode_compatible
class IssueFlowInfo(models.Model):
    issue = models.ForeignKey(IssueInfo, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    member = models.ForeignKey(MemberInfo, null=True, on_delete=models.DO_NOTHING)
    behavior = models.SmallIntegerField(choices=BEHAVIOR_TYPE, default=1, verbose_name='行为类型')
    status = models.SmallIntegerField(choices=ISSUE_STATUS, default=1)
    url = models.CharField(max_length=128, null=True, verbose_name='处理地址')
    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if len(self.comment) > 20:
            return '{0}...'.format(self.comment[:20])
        else:
            return self.comment

    class Meta:
        verbose_name = u"问题工单"
        verbose_name_plural = verbose_name
        db_table = u'sca_issue_flow'


@python_2_unicode_compatible
class IssueWhiteListInfo(models.Model):
    issue = models.ForeignKey(IssueInfo, on_delete=models.CASCADE)
    operator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='操作人')
    comment = models.CharField(max_length=500, verbose_name='忽略说明')
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

    class Meta:
        verbose_name = u"工单白名单"
        verbose_name_plural = verbose_name
        db_table = u'sca_issue_whitelist'
