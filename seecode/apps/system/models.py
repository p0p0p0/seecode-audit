# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.contenttypes.models import ContentType
from django_celery_beat.models import CrontabSchedule
from django_celery_beat.models import IntervalSchedule
from django.contrib.auth.models import User

from seecode.libs.core.enum import SYSLOG_LEVEL
from seecode.libs.core.enum import SYSLOG_TYPE
from seecode.libs.core.enum import SCHED_TYPE
from seecode.libs.core.enum import WIDGET_TYPE
from seecode.libs.core.enum import EMPLOYEE_STATUS
from seecode.libs.core.enum import GENDER_TYPE


@python_2_unicode_compatible
class TagInfo(models.Model):
    name = models.CharField(max_length=128, verbose_name='名称')
    description = models.TextField(null=True, verbose_name='描述')
    parent = models.ForeignKey('self', null=True, verbose_name='父亲分类', on_delete=models.DO_NOTHING)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"Tag"
        verbose_name_plural = verbose_name
        db_table = u'sca_common_tag'


@python_2_unicode_compatible
class SyslogInfo(models.Model):
    title = models.CharField(max_length=128, verbose_name='标题')
    description = models.TextField(null=True, verbose_name='消息内容')
    stack_trace = models.TextField(null=True, verbose_name='堆栈信息')
    module = models.ForeignKey(ContentType, null=True, verbose_name='问题模块', on_delete=models.CASCADE)
    object_id = models.IntegerField(null=True)
    ipv4 = models.CharField(max_length=20, null=True, verbose_name='ipv4')
    type = models.SmallIntegerField(choices=SYSLOG_TYPE, default=1)
    level = models.SmallIntegerField(choices=SYSLOG_LEVEL, default=4, verbose_name='日志级别')
    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = u"Syslog"
        verbose_name_plural = verbose_name
        db_table = u'sca_common_syslog'


@python_2_unicode_compatible
class SchedInfo(models.Model):
    name = models.CharField(max_length=128, verbose_name='标题')
    type = models.SmallIntegerField(choices=SCHED_TYPE, default=1)
    crontab = models.ForeignKey(CrontabSchedule, null=True, on_delete=models.CASCADE)
    interval = models.ForeignKey(IntervalSchedule, null=True, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"Syslog"
        verbose_name_plural = verbose_name
        db_table = u'sca_common_sched'


@python_2_unicode_compatible
class ConfigInfo(models.Model):
    site = models.CharField(max_length=256, verbose_name='站点名称')
    content = models.TextField(null=True, verbose_name='系统配置')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.site

    class Meta:
        verbose_name = u"系统配置表"
        verbose_name_plural = verbose_name
        db_table = u'sca_common_config'


@python_2_unicode_compatible
class LanguageInfo(models.Model):
    name = models.CharField(max_length=16, verbose_name='名称')
    suffix = models.CharField(max_length=255, verbose_name='后缀', null=True)
    key = models.TextField(null=True, verbose_name='key')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"开发语言"
        verbose_name_plural = verbose_name
        db_table = u'sca_conf_language'
