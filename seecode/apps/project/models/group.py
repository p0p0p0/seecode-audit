# coding: utf-8
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User

from seecode.apps.project.models.member import MemberInfo
from seecode.libs.core.enum import APP_TYPE


@python_2_unicode_compatible
class GroupInfo(models.Model):
    """
    https://git.gitlab.com/api/v3/groups/1994

    {
        id": 1994,
        "name": "example",
        "path": "goc",
        "description": "",
        "visibility_level": 0,
        "lfs_enabled": true,
        "avatar_url": null,
        "web_url": "https://git.gitlab.com/groups/goc",
        "request_access_enabled": true,
        "full_name": "example",
        "full_path": "goc",
        "parent_id": null,
        "projects": [],
        "shared_projects": []
    }
    """
    git_id = models.IntegerField(null=True)
    name = models.CharField(max_length=128)
    path = models.CharField(max_length=128, null=True)
    description = models.CharField(max_length=500, null=True)
    web_url = models.CharField(max_length=255, null=True)
    full_name = models.CharField(max_length=128, null=True)
    full_path = models.CharField(max_length=128, null=True)
    parent_id = models.IntegerField(null=True)
    visibility_level = models.IntegerField(default=0)

    type = models.SmallIntegerField(default=1, choices=APP_TYPE)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    members = models.ManyToManyField(MemberInfo, db_table='r_group_member', related_name='group')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = u"项目组"
        verbose_name_plural = verbose_name
        db_table = u'sca_gitlab_group'

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class GroupPermissionInfo(models.Model):
    """

    """
    group = models.ForeignKey(GroupInfo, on_delete=models.CASCADE)
    member = models.ForeignKey(MemberInfo, on_delete=models.CASCADE)
    access_level = models.IntegerField(null=True)
    expires_at = models.DateTimeField(null=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"项目组权限"
        verbose_name_plural = verbose_name
        db_table = u'sca_gitlab_group_member_permission'
