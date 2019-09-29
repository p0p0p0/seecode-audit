# -*- coding: utf-8

from django.urls import path
from rest_framework import routers
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer
from rest_framework_swagger.renderers import OpenAPIRenderer

from seecode.apps.api.v2.views.node import services
from seecode.apps.api.v2.views.node import host
from seecode.apps.api.v2.views.scan import statistics
from seecode.apps.api.v2.views.scan import task
from seecode.apps.api.v2.views.scan import issue
from seecode.apps.api.v2.views.scan import project
from seecode.apps.api.v2.views.sys import log
from seecode.apps.api.v2.views.sys import upgrade

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()

schema_view = get_schema_view(title='Users API', renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path(r'node/host/', host.HostSet.as_view()),
    path(r'node/services/', services.ServiceSet.as_view()),
    path(r'task/<int:task_id>/', task.TaskSet.as_view()),
    path(r'task/<int:task_id>/status/', task.TaskSet.as_view()),
    path(r'task/<int:task_id>/component/', statistics.ComponentSet.as_view()),
    path(r'task/<int:task_id>/statistic/', statistics.FileStatisticSet.as_view()),
    path(r'task/<int:task_id>/issue/', issue.IssueSet.as_view()),
    path(r'issue/<int:issue_id>/callback/', issue.IssueCallbackSet.as_view()),
    path(r'upgrade/version/', upgrade.UpgradeSet.as_view()),
    path(r'scan/add/', project.ProjectSet.as_view()),
    path(r'sys/log/', log.SysLogSet.as_view()),
]
