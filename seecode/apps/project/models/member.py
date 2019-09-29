# coding: utf-8

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class MemberInfo(models.Model):
    """
    https://git.gitlab.com/api/v3/users/100
    {
        "id": 100,
        "name": "张三",
        "username": "zhangsan",
        "state": "blocked",
        "avatar_url": "https://secure.gravatar.com/avatar/2b5f5d695e5b52f5e0c2bd88c45b11ea?s=80&d=identicon",
        "web_url": "https://git.gitlab.com/zhangsan",
        "created_at": "2015-05-11T06:01:39.142Z",
        "bio": null,
        "location": null,
        "skype": "",
        "linkedin": "",
        "twitter": "",
        "website_url": "",
        "organization": null
    }
    """
    git_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=64)
    username = models.CharField(max_length=200)
    state = models.CharField(max_length=32, null=True)
    web_url = models.CharField(max_length=200)
    email = models.CharField(max_length=200, null=True)
    gitlab_created_at = models.DateTimeField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"成员信息表"
        verbose_name_plural = verbose_name
        db_table = u'sca_gitlab_member'
