# coding: utf-8

from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from seecode.apps.project.models.group import GroupInfo
from seecode.apps.project.models.member import MemberInfo
from seecode.libs.core.enum import PROJECT_TYPE
from seecode.libs.core.enum import REPOSITORY_TYPE
from seecode.libs.core.enum import ICON_TYPE


@python_2_unicode_compatible
class ProjectInfo(models.Model):
    """
    {
        "id": 9770,
        "description": "description",
        "default_branch": "master",
        "tag_list": [],
        "public": false,
        "archived": false,
        "visibility_level": 0,
        "ssh_url_to_repo": "git@git.gitlab.com:demo_group/render-goods.git",
        "http_url_to_repo": "https://git.gitlab.com/demo_group/render-goods.git",
        "web_url": "https://git.gitlab.com/demo_group/render-goods",
        "name": "render-goods",
        "name_with_namespace": "DEMO_GROUP / render-goods",
        "path": "render-goods",
        "path_with_namespace": "demo_group/render-goods",
        "resolve_outdated_diff_discussions": false,
        "container_registry_enabled": true,
        "issues_enabled": true,
        "merge_requests_enabled": true,
        "wiki_enabled": true,
        "builds_enabled": true,
        "snippets_enabled": true,
        "created_at": "2018-03-20T04:44:46.571Z",
        "last_activity_at": "2019-03-20T04:44:46.571Z",
        "shared_runners_enabled": false,
        "lfs_enabled": true,
        "creator_id": 1114,
        "namespace": {
            "id": 238,
            "name": "DEMO_GROUP",
            "path": "demo_group",
            "kind": "group",
            "full_path": "demo_group",
            "parent_id": null
        },
        "avatar_url": null,
        "star_count": 0,
        "forks_count": 0,
        "open_issues_count": 0,
        "public_builds": true,
        "shared_with_groups": [],
        "only_allow_merge_if_build_succeeds": false,
        "request_access_enabled": false,
        "only_allow_merge_if_all_discussions_are_resolved": false,
        "permissions": {
            "project_access": null,
            "group_access": {
                "access_level": 20,
                "notification_level": 3
            }
        }
    }
    """
    git_id = models.IntegerField(null=True)
    git_created_at = models.DateTimeField(null=True)
    git_last_activity_at = models.DateTimeField(null=True)
    ssh_url_to_repo = models.CharField(max_length=255, null=True)
    http_url_to_repo = models.CharField(max_length=255, null=True)
    web_url = models.CharField(max_length=255, null=True)
    default_branch = models.CharField(max_length=128, null=True)
    name = models.CharField(max_length=128)
    path = models.CharField(max_length=128)
    file_hash = models.CharField(max_length=128, null=True)
    file_size = models.IntegerField(default=0, null=True)
    file_origin_name = models.CharField(max_length=128, null=True)
    path_with_namespace = models.CharField(max_length=255, null=True)
    creator_id = models.IntegerField(null=True)
    description = models.CharField(max_length=500, null=True)
    star_count = models.IntegerField(default=0)
    forks_count = models.IntegerField(default=0)
    open_issues_count = models.IntegerField(default=0)
    visibility_level = models.IntegerField(default=0)
    issues_enabled = models.BooleanField(default=True)

    members = models.ManyToManyField(MemberInfo, db_table='r_project_member', related_name='project')

    group = models.ForeignKey(GroupInfo, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    type = models.SmallIntegerField(choices=PROJECT_TYPE, default=1)

    is_new = models.BooleanField(default=False)
    is_archive = models.BooleanField(default=False)
    # is_scan = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"项目列表"
        verbose_name_plural = verbose_name
        db_table = u'sca_gitlab_project'


@python_2_unicode_compatible
class ProjectPermissionInfo(models.Model):
    """

    """
    project = models.ForeignKey(ProjectInfo, on_delete=models.CASCADE)
    member = models.ForeignKey(MemberInfo, on_delete=models.CASCADE)
    access_level = models.IntegerField(null=True)
    expires_at = models.DateTimeField(null=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.member

    class Meta:
        verbose_name = u"项目权限"
        verbose_name_plural = verbose_name
        db_table = u'sca_gitlab_project_member_permission'


@python_2_unicode_compatible
class RepositoryInfo(models.Model):
    """
    {
        "name": "master",
        "merged": false,
        "protected": true,
        "developers_can_push": false,
        "developers_can_merge": false,
        "commit": {
          "author_email": "john@example.com",
          "author_name": "John Smith",
          "authored_date": "2012-06-27T05:51:39-07:00",
          "committed_date": "2012-06-28T03:44:20-07:00",
          "committer_email": "john@example.com",
          "committer_name": "John Smith",
          "id": "7b5c3cc8be40ee161ae89a06bba6229da1032a0c",
          "short_id": "7b5c3cc",
          "title": "add projects API",
          "message": "add projects API",
          "parent_ids": [
            "4ad91d3c1144c406e50c7b33bae684bd6837faf8"
          ]
        }
      }

    """
    name = models.CharField(max_length=128)
    merged = models.BooleanField(default=False)
    protected = models.BooleanField(default=False)
    developers_can_push = models.BooleanField(default=False)
    developers_can_merge = models.BooleanField(default=False)

    last_commit_id = models.CharField(max_length=40, null=True)
    last_short_id = models.CharField(max_length=8, null=True)
    last_author_email = models.CharField(max_length=255, null=True)
    last_author_name = models.CharField(max_length=255, null=True)
    last_title = models.CharField(max_length=255, null=True)
    committed_date = models.DateTimeField(null=True)

    project = models.ForeignKey(ProjectInfo, on_delete=models.CASCADE)
    type = models.SmallIntegerField(choices=REPOSITORY_TYPE, default=1)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"代码分支"
        verbose_name_plural = verbose_name
        db_table = u'sca_gitlab_repository'


@python_2_unicode_compatible
class ProjectHistoryInfo(models.Model):
    """
    """
    project = models.ForeignKey(ProjectInfo, on_delete=models.CASCADE)
    type = models.SmallIntegerField(choices=ICON_TYPE, default=1)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    is_first = models.BooleanField(default=False)
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = u"项目历史表"
        verbose_name_plural = verbose_name
        db_table = u'sca_gitlab_project_history'
