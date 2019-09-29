# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from seecode.apps.system.models import LanguageInfo
from seecode.apps.system.models import TagInfo
from seecode.libs.core.enum import ATTRIBUTE_TYPE
from seecode.libs.core.enum import COMPONENT_MATCH_TYPE
from seecode.libs.core.enum import NATURE_TYPE
from seecode.libs.core.enum import RISK_TYPE
from seecode.libs.core.enum import TACTIC_MATCH_TYPE
from seecode.libs.core.enum import TACTIC_TYPE


@python_2_unicode_compatible
class EngineInfo(models.Model):
    name = models.CharField(max_length=16, verbose_name='名称')
    module_name = models.TextField(max_length=64)
    enable = models.BooleanField(default=True)
    url = models.TextField(max_length=255, null=True)
    is_customize = models.BooleanField(default=True)
    description = models.TextField(null=True)
    whitelist_count = models.IntegerField(default=0)
    blacklist_count = models.IntegerField(default=0)
    config = models.TextField(null=True)
    revision = models.FloatField(default=1.0)

    updated_at = models.DateTimeField(verbose_name='更新时间', auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"引擎列表"
        verbose_name_plural = verbose_name
        db_table = u'sca_engine'


@python_2_unicode_compatible
class VulnCategoryInfo(models.Model):
    name = models.CharField(max_length=64)
    tag = models.CharField(max_length=64, null=True)
    key = models.CharField(max_length=64, null=True)
    parent = models.ForeignKey('self', null=True, verbose_name='父亲分类', on_delete=models.DO_NOTHING)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"漏洞类别"
        verbose_name_plural = verbose_name
        db_table = u'sca_vuln_category'


@python_2_unicode_compatible
class VulnInfo(models.Model):
    cate = models.ForeignKey(VulnCategoryInfo, on_delete=models.CASCADE)
    origin = models.ForeignKey(TagInfo, on_delete=models.CASCADE, null=True, verbose_name='来源')
    title = models.CharField(max_length=255)
    description = models.TextField()
    solution = models.TextField(null=True)
    reference = models.TextField(null=True)

    risk = models.SmallIntegerField(choices=RISK_TYPE, default=3)
    hit = models.IntegerField(default=0)
    impact_version = models.CharField(max_length=64, null=True)
    cnnvd = models.CharField(max_length=255, null=True)
    cnvd = models.CharField(max_length=255, null=True)
    cve = models.CharField(max_length=255, null=True)
    bugtraq = models.CharField(max_length=255, null=True)
    tags = models.ManyToManyField(TagInfo, db_table='r_vuln_tag', related_name='vuln')

    find_time = models.DateField(verbose_name='发现时间', null=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = u"漏洞知识库"
        verbose_name_plural = verbose_name
        db_table = u'sca_vuln_info'


@python_2_unicode_compatible
class TacticInfo(models.Model):
    lang = models.ForeignKey(LanguageInfo, null=True, on_delete=models.CASCADE)
    engine = models.ForeignKey(EngineInfo, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    vuln = models.ForeignKey(VulnInfo, null=True, on_delete=models.CASCADE)
    tags = models.ManyToManyField(TagInfo, db_table='r_tactic_tag', related_name='tactic')
    revision = models.FloatField(default=1.0)

    key = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True, verbose_name='安全描述')
    solution = models.TextField(null=True, verbose_name='修复意见')
    type = models.SmallIntegerField(choices=TACTIC_TYPE, default=3)

    risk = models.SmallIntegerField(choices=RISK_TYPE, default=3)
    risk_scope = models.FloatField(default=0.0)
    nature_type = models.SmallIntegerField(choices=NATURE_TYPE, default=1, verbose_name='名单类型')
    attribution_type = models.SmallIntegerField(choices=ATTRIBUTE_TYPE, default=1, verbose_name='归属类型')

    rule_match_type = models.SmallIntegerField(choices=TACTIC_MATCH_TYPE, default=1)
    rule_value = models.CharField(max_length=255, null=True)
    rule_regex = models.TextField(null=True)
    component_name = models.CharField(max_length=255, null=True)
    rule_regex_flag = models.CharField(max_length=32, null=True)

    plugin_name = models.CharField(max_length=64, null=True, verbose_name='文件名')
    plugin_module_name = models.CharField(max_length=64, null=True, verbose_name='模块')
    plugin_content = models.TextField(null=True, verbose_name='内容')

    scm_conf = models.CharField(max_length=255, null=True, verbose_name='SCM 同步配置')
    alarm_conf = models.TextField(max_length=255, null=True, verbose_name='告警配置')
    alarm_title = models.TextField(max_length=255, null=True, verbose_name='告警标题')

    is_active = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"策略内容"
        verbose_name_plural = verbose_name
        db_table = u'sca_tactic'

