# coding: utf-8
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from seecode.libs.core.enum import SERVICE_STATUS_TYPE, NODE_ROLE_TYPE
from seecode.libs.core.enum import CHANGELOG_MODULE_TYPE, CHANGELOG_ACTION_TYPE


@python_2_unicode_compatible
class HostInfo(models.Model):
    is_role_ui = models.BooleanField(default=False)
    is_role_client = models.BooleanField(default=False)
    hostname = models.CharField(max_length=32, null=True)
    ipv4 = models.CharField(max_length=64)
    ipv6 = models.CharField(max_length=64, null=True)
    ui_version = models.CharField(max_length=32, null=True)
    client_version = models.CharField(max_length=32, null=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.hostname

    class Meta:
        verbose_name = u"集群节点"
        verbose_name_plural = verbose_name
        db_table = u'sca_node_host'


@python_2_unicode_compatible
class ServiceInfo(models.Model):
    name = models.CharField(max_length=32, verbose_name='名称')
    key = models.CharField(max_length=128, verbose_name='关键字')
    role = models.SmallIntegerField(choices=NODE_ROLE_TYPE, verbose_name='角色')
    process_keyword = models.CharField(max_length=255, verbose_name='进程关键字')
    description = models.TextField(null=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"配置服务"
        verbose_name_plural = verbose_name
        db_table = u'sca_node_service'


@python_2_unicode_compatible
class HostServiceInfo(models.Model):
    host = models.ForeignKey(HostInfo, on_delete=models.CASCADE)
    service = models.ForeignKey(ServiceInfo, on_delete=models.CASCADE)
    ppid = models.IntegerField(verbose_name='父进程', null=True)
    pid = models.IntegerField(verbose_name='进程', null=True)
    status = models.SmallIntegerField(choices=SERVICE_STATUS_TYPE, verbose_name='状态')

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"节点服务"
        verbose_name_plural = verbose_name
        db_table = u'sca_node_host_service'


@python_2_unicode_compatible
class UpgradePackageInfo(models.Model):
    name = models.CharField(max_length=32, verbose_name='名称')
    version = models.CharField(max_length=32, verbose_name='版本')
    changelog = models.TextField(null=True, verbose_name='历史')
    description = models.TextField(null=True, verbose_name='描述')
    hash = models.CharField(max_length=255, verbose_name='hash')
    path = models.CharField(max_length=255, null=True)
    is_archive = models.BooleanField(default=False)
    role = models.SmallIntegerField(choices=NODE_ROLE_TYPE, verbose_name='角色')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"升级包"
        verbose_name_plural = verbose_name
        db_table = u'sca_upgrade_package'


@python_2_unicode_compatible
class UpgradeVersionInfo(models.Model):
    major = models.IntegerField(default=1)
    minor = models.IntegerField(default=0)
    revision = models.IntegerField(default=0)
    role = models.SmallIntegerField(choices=NODE_ROLE_TYPE, verbose_name='角色')
    
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = u"升级版本"
        verbose_name_plural = verbose_name
        db_table = u'sca_upgrade_version'


@python_2_unicode_compatible
class UpgradeChangelogInfo(models.Model):
    is_archive = models.BooleanField(default=False)
    action = models.SmallIntegerField(choices=CHANGELOG_ACTION_TYPE)
    module = models.SmallIntegerField(choices=CHANGELOG_MODULE_TYPE, verbose_name='模块')
    version = models.CharField(max_length=16, null=True)
    description = models.TextField()

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = u"升级版本"
        verbose_name_plural = verbose_name
        db_table = u'sca_upgrade_changelog'
