# coding: utf-8
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from seecode.apps.project.models.item import ProjectInfo
from seecode.apps.project.models.item import RepositoryInfo
from seecode.apps.system.models import LanguageInfo
from seecode.libs.core.enum import PROJECT_STATUS


@python_2_unicode_compatible
class ApplicationInfo(models.Model):
    """

    """
    project = models.ForeignKey(ProjectInfo, on_delete=models.CASCADE)
    repo = models.ForeignKey(RepositoryInfo, null=True, on_delete=models.CASCADE)
    lang = models.ForeignKey(LanguageInfo, null=True, on_delete=models.CASCADE)

    module_name = models.CharField(max_length=128)
    app_name = models.CharField(max_length=128, null=True)
    version = models.CharField(max_length=128, null=True)

    code_total = models.IntegerField(blank=True, default=0)
    size = models.IntegerField(null=True, default=0)
    report_url = models.CharField(max_length=500, null=True)
    ignore_count = models.IntegerField(default=0, verbose_name='忽略漏洞数')

    critical = models.IntegerField(default=0)
    high = models.IntegerField(default=0)
    medium = models.IntegerField(default=0)
    low = models.IntegerField(default=0)
    info = models.IntegerField(default=0)
    risk_scope = models.FloatField(default=0, verbose_name='风险分数')

    status = models.SmallIntegerField(choices=PROJECT_STATUS, default=1)
    is_archive = models.BooleanField(default=False)
    last_scan_time = models.DateTimeField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.app_name

    class Meta:
        unique_together = ('module_name', )
        verbose_name = u"应用名称"
        verbose_name_plural = verbose_name
        db_table = u'sca_application'


@python_2_unicode_compatible
class DependentInfo(models.Model):
    app = models.ForeignKey(ApplicationInfo, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    file_name = models.CharField(max_length=255)
    full_path = models.CharField(max_length=255)
    group_id = models.CharField(max_length=128, null=True)  # pom.xml
    artifact_id = models.CharField(max_length=128, null=True)  # pom.xml
    version = models.CharField(max_length=32, null=True)
    new_version = models.CharField(max_length=32, null=True)
    description = models.CharField(max_length=200, null=True)
    is_archive = models.BooleanField(default=False)
    language = models.CharField(max_length=16, null=True, verbose_name='')

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"项目依赖包"
        verbose_name_plural = verbose_name
        db_table = u'sca_application_dependent'


@python_2_unicode_compatible
class FileStatisticsInfo(models.Model):
    app = models.ForeignKey(ApplicationInfo, on_delete=models.CASCADE)
    language = models.CharField(max_length=32)
    files = models.IntegerField(blank=True, null=True)
    blank = models.IntegerField(blank=True, null=True)
    comment = models.IntegerField(blank=True, null=True)
    code = models.IntegerField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.language

    class Meta:
        verbose_name = u"扫描统计"
        verbose_name_plural = verbose_name
        db_table = u'sca_application_statistics'
